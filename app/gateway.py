from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
import time, threading
lock=threading.Lock()
counts={s:0 for s in (200,502,503,504)}
bounds=[.005,.01,.025,.05,.1,.25,.5,1,2,5,10]
buckets=[0]*len(bounds)
total=0; duration=0.0
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global total,duration
        if self.path=='/metrics':
            with lock:
                lines=['# TYPE http_requests_total counter']+[f'http_requests_total{{status="{s}",method="GET"}} {n}' for s,n in counts.items()]
                lines+=['# TYPE http_request_duration_seconds histogram']+[f'http_request_duration_seconds_bucket{{le="{b}"}} {n}' for b,n in zip(bounds,buckets)]
                lines += [f'http_request_duration_seconds_bucket{{le="+Inf"}} {total}',f'http_request_duration_seconds_count {total}',f'http_request_duration_seconds_sum {duration}']
            status=200; body=('\n'.join(lines)+'\n').encode(); content='text/plain; version=0.0.4'
        elif self.path=='/healthz':
            status=200; body=b'ok'; content='text/plain'
        else:
            start=time.monotonic()
            try:
                with urlopen('http://inventory-api:8080/',timeout=3) as response:
                    status=response.status; body=response.read()
            except Exception as exc:
                print(f'Upstream request failed: {exc}',flush=True)
                status=503; body=b'Inventory service temporarily unavailable'
            elapsed=time.monotonic()-start; content='application/json' if status==200 else 'text/plain'
            with lock:
                counts[status]=counts.get(status,0)+1; total+=1; duration+=elapsed
                for i,b in enumerate(bounds):
                    if elapsed<=b: buckets[i]+=1
        self.send_response(status); self.send_header('Content-Type',content); self.send_header('Content-Length',str(len(body))); self.end_headers()
        try: self.wfile.write(body)
        except BrokenPipeError: pass
ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
