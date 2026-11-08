from __future__ import annotations

import base64
import hashlib
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

code_verifier = secrets.token_urlsafe(43)
code_challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest())
    .rstrip(b"=")
    .decode("ascii")
)
CCM = "S256"

ADDRESS = "127.0.0.1"
PORT = 0


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/auth/callback"):
            self.send_response(200)
            url = urlparse(self.path)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h1>Authentication Successful. <br> You can close this window.</h1>"
            )
            data = parse_qs(url.query)
            return data
        else:
            self.send_error(404, "Not Found")


def CreateCallbackServer():
    return HTTPServer((ADDRESS, PORT), CallbackHandler)
