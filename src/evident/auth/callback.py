import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

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
            with open("data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        else:
            self.send_error(404, "Not Found")


server = HTTPServer((ADDRESS, PORT), CallbackHandler)
port = server.server_address[1]
server.serve_forever()

REDIRECT_URI = f"http://{ADDRESS}:{PORT}/auth/callback"


from platformdirs import PlatformDirs

dirs = PlatformDirs(appname="evident", appauthor=False)

print(dirs.user_config_dir)
