#!/usr/bin/env python3
"""
BALLS FIGHTING Z - local server.

The important part is the no-cache headers. Python's built-in
"http.server -m" sends no Cache-Control, so browsers apply *heuristic*
caching and happily keep serving a STALE copy of the game. That is how
you end up editing the file, reloading, and seeing the old build.

This server always tells the browser to re-fetch.
"""
import http.server
import socketserver
import os
import sys

PORT = 8777
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # never cache - always serve the file as it is right now
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Ball-Fighting-Z", "live")
        super().end_headers()

    def send_response(self, code, message=None):
        # quieter console
        sys.stdout.write("%s - %s\n" % (self.address_string(), code))
        sys.stdout.flush()
        super().send_response(code, message)

    def log_message(self, format, *args):
        pass


class Server(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("127.0.0.1", PORT), Handler) as httpd:
        print("BALLS FIGHTING Z  ->  http://localhost:%d/index.html" % PORT)
        print("Serving with NO-CACHE. Keep this window open. Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")