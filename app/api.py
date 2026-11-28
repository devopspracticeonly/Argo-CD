from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, time, os
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/healthz":
            time.sleep(float(os.environ.get("PROCESSING_INTERVAL", "0.02")))
        body=json.dumps({'checkouts':[{'id':101,'status':'confirmed'}]}).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)
ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
