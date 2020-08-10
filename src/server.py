import http.server
import time
import requests
import jwt
import secrets
import datetime
import os

ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
USERNAME = os.environ.get("USERNAME")
SECRET = os.environ.get("SECRET")

class ProxyServer(http.server.BaseHTTPRequestHandler):
    # Time the server was started
    start_time = time.time()

    # Number of Proxy requests processed
    request_count = 0

    def do_POST(self):
        print(f"POST {self.path} from ({self.client_address[0]}, {self.client_address[1]})")

        ProxyServer.request_count += 1
        
        dt = datetime.datetime.now()
        dt.replace(tzinfo=datetime.timezone.utc)
        claims = {
            "iat": time.time(),
            "jti": secrets.token_hex(32),
            "payload": {
                "user": USERNAME,
                "date": dt.strftime("%Y-%m-%d %H:%M:%SZ")
            }
        }
        request_body = self.rfile.read(int(self.headers['Content-Length']))
        self.headers["x-my-jwt"] = jwt.encode(claims, SECRET)

        r = requests.post(ENDPOINT_URL, headers = self.headers, data = request_body)

        self.send_response(r.status_code)
        [self.send_header(key, r.headers[key]) for key in r.headers]
        self.end_headers()
        self.wfile.write(bytearray(r.text, r.encoding))


    def do_GET(self):
        print(f"GET {self.path} from ({self.client_address[0]}, {self.client_address[1]})")

        if (self.path == "/status"):
            current_time = time.time()
            html = f"""<!DOCTYPE html>
<html>
<head>
<title>Status</title>
</head>
<body>
Time from start: {current_time - ProxyServer.start_time} secs<br>
Number of requests processed: {ProxyServer.request_count}
</body>
</html>"""
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytearray(html, "ascii"))
            return

        self.send_error(404)
