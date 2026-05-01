"""Minimal HTTP health-check server for Render free-tier web service."""

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass  # silence logs


def start_health_server(port: int = 10000) -> None:
    """Start a background HTTP server on *port* for Render health checks."""
    srv = HTTPServer(("0.0.0.0", port), _Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
