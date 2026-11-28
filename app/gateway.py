from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
from threading import Lock
import time
lock=Lock(); counts={}; buckets=[.05,.1,.25,.5,1,2,5,10]; hist=[0]*len(buckets); total=0; elapsed=0
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global total,elapsed
        if self.path == '/metrics':
            with lock:
                lines=['# TYPE http_requests_total counter']+[f'http_requests_total{{status="{k}"}} {v}' for k,v in counts.items()]
                lines+=['# TYPE http_request_duration_seconds histogram']+[f'http_request_duration_seconds_bucket{{le="{b}"}} {v}' for b,v in zip(buckets,hist)]+[f'http_request_duration_seconds_bucket{{le="+Inf"}} {total}',f'http_request_duration_seconds_count {total}',f'http_request_duration_seconds_sum {elapsed}']
            self.send_response(200); self.end_headers(); self.wfile.write(('\n'.join(lines)+'\n').encode()); return
        start=time.monotonic()
        try:
            with urlopen('http://order-api:8080/',timeout=3) as response: body=response.read(); status=response.status
        except Exception: status=503; body=b'Order service unavailable\n'
        duration=time.monotonic()-start
        with lock:
            counts[status]=counts.get(status,0)+1; total+=1; elapsed+=duration
            for i,b in enumerate(buckets): hist[i]+=int(duration<=b)
        self.send_response(status); self.end_headers(); self.wfile.write(body)
ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
