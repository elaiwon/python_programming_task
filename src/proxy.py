import http.server
import socketserver
import signal
import sys
import os
import server

PORT = int(os.environ.get("HTTP_PORT")) if os.environ.get("HTTP_PORT") else 8000

with socketserver.TCPServer(("", PORT), server.ProxyServer) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()