"""Replay server: serves recorded responses for any host over HTTPS 443 and HTTP 80.

Run: sudo python3 speed_lab/serve.py  (background). Chromium maps every host to 127.0.0.1 with
--host-resolver-rules="MAP * 127.0.0.1" and --ignore-certificate-errors.
Overrides come from speed_lab/ACTIVE_VARIANT (a variant dir name) if set. Each served response is
logged to results/serve.log as JSON with the run tag from speed_lab/ACTIVE_RUN.
"""
import gzip, json, os, ssl, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab import STORE, VARIANTS, key, load_index, norm, get_active, ROOT

LOG = os.path.join(ROOT, "results", "serve.log")
RUN = os.path.join(ROOT, "ACTIVE_RUN")
DROP_HEADERS = {"content-encoding", "content-length", "transfer-encoding", "connection", "alt-svc", "strict-transport-security", "content-security-policy", "content-security-policy-report-only", "cross-origin-opener-policy", "report-to", "nel", "set-cookie", "expect-ct", "x-frame-options"}
KEEP_HEADERS = {"content-type", "cache-control", "vary", "access-control-allow-origin", "access-control-allow-credentials", "access-control-expose-headers", "location", "last-modified", "etag", "x-content-type-options", "timing-allow-origin", "cross-origin-resource-policy", "expires", "pragma"}
TEXT = ("text/", "application/javascript", "application/x-javascript", "application/json", "image/svg", "application/xml")
_base = load_index(STORE)
_var_cache = {}
_lock = threading.Lock()


def variant_index():
    name = get_active()
    if not name:
        return None, None
    d = os.path.join(VARIANTS, name)
    m = os.path.getmtime(os.path.join(d, "index.json")) if os.path.exists(os.path.join(d, "index.json")) else 0
    with _lock:
        c = _var_cache.get(name)
        if not c or c[0] != m:
            c = (m, load_index(d)); _var_cache[name] = c
    return name, c[1]


def lookup(url):
    k = key(url)
    name, vidx = variant_index()
    if vidx and k in vidx:
        return vidx[k], os.path.join(VARIANTS, name), "variant"
    if k in _base:
        return _base[k], STORE, "base"
    # fuzzy: same host and path, ignore query
    s = urlsplit(url)
    want = (s.netloc.lower(), s.path or "/")
    for src, d, tag in ((vidx, os.path.join(VARIANTS, name) if name else None, "variant-fuzzy"), (_base, STORE, "base-fuzzy")):
        if not src: continue
        for e in src.values():
            u = urlsplit(e["url"])
            if (u.netloc, u.path or "/") == want:
                return e, d, tag
    return None, None, None


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _serve(self, with_body=True):
        host = self.headers.get("Host", "")
        scheme = "https" if isinstance(self.server, HTTPSServer) else "http"
        url = f"{scheme}://{host}{self.path}"
        e, d, tag = lookup(url)
        run = open(RUN).read().strip() if os.path.exists(RUN) else ""
        if not e:
            body = b"not recorded"
            self.send_response(404); self.send_header("Content-Type", "text/plain"); self.send_header("Content-Length", str(len(body))); self.end_headers()
            if with_body: self.wfile.write(body)
            self._log(run, url, 404, 0, "miss", None)
            return
        body = open(os.path.join(d, e["file"]), "rb").read() if e.get("file") else b""
        ct = e["headers"].get("content-type", "application/octet-stream")
        enc = None
        if body and e["headers"].get("content-encoding") and "gzip" in (self.headers.get("Accept-Encoding") or ""):
            body = gzip.compress(body, 6); enc = "gzip"
        self.send_response(e["status"] if e["status"] < 600 else 200)
        for k, v in e["headers"].items():
            if k.lower() not in KEEP_HEADERS or "\n" in v or "\r" in v: continue
            self.send_header(k, v)
        if enc: self.send_header("Content-Encoding", enc)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if with_body and body:
            try: self.wfile.write(body)
            except Exception: pass
        self._log(run, url, e["status"], len(body), tag, e.get("type"))

    def _log(self, run, url, status, wire, tag, rtype):
        with _lock, open(LOG, "a") as f:
            f.write(json.dumps({"t": time.time(), "run": run, "url": url[:300], "status": status, "wire": wire, "src": tag, "type": rtype}) + "\n")

    def do_GET(self): self._serve()
    def do_HEAD(self): self._serve(with_body=False)
    def do_POST(self): self._serve()
    def do_OPTIONS(self):
        self.send_response(204); self.send_header("Access-Control-Allow-Origin", "*"); self.send_header("Access-Control-Allow-Headers", "*"); self.send_header("Access-Control-Allow-Methods", "*"); self.send_header("Content-Length", "0"); self.end_headers()


class HTTPSServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class HTTPServerPlain(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(os.path.join(ROOT, "cert.pem"), os.path.join(ROOT, "key.pem"))
    https = HTTPSServer(("127.0.0.1", 443), H)
    https.socket = ctx.wrap_socket(https.socket, server_side=True)
    http = HTTPServerPlain(("127.0.0.1", 80), H)
    threading.Thread(target=http.serve_forever, daemon=True).start()
    print("replay server on 127.0.0.1:443 and :80, store entries", len(_base), flush=True)
    https.serve_forever()


if __name__ == "__main__":
    main()
