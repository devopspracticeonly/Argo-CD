from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Order API available\n")
ThreadingHTTPServer(("0.0.0.0",8080),Handler).serve_forever()
