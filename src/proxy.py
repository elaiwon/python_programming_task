import http.server
import socketserver
import signal
import sys
import server
import os

PORT = os.environ.get("HTTP_PORT") or 8000

with socketserver.TCPServer(("", PORT), server.ProxyServer) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()