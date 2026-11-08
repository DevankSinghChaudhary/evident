from __future__ import annotations

from evident.auth import CreateCallbackServer

# CONSTANTS AND SERVER CREATION
server = CreateCallbackServer()
HOST, PORT = server.server_address
REDIRECT_URI = f"http://{HOST}:{PORT}/auth/callback"

server.handle_request()
server.server_close()
