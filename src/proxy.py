import http.server
import socketserver
import signal
import sys
import server

PORT = 8000

with socketserver.TCPServer(("", PORT), server.ProxyServer) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()