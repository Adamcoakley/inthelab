#!/usr/bin/env python3
"""
inthelab test server.

Shows which server answered your request: its name, Availability Zone and
private IP. It uses only Python's standard library, so there is nothing to
install. Run it with:

    sudo python3 hello-server.py          (port 80, needs sudo)
    python3 hello-server.py 8000          (any other port, for testing)
"""
import sys
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socket import gethostname

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 80
IMDS = "http://169.254.169.254/latest"
STARTED = time.time()

served = 0
info = {}
last_try = 0.0

AZ_COLOURS = {"a": "#22C7B8", "b": "#F5A524", "c": "#8B7BF0"}


def metadata(path, token):
    req = urllib.request.Request(f"{IMDS}/meta-data/{path}",
                                 headers={"X-aws-ec2-metadata-token": token})
    return urllib.request.urlopen(req, timeout=1).read().decode()


def load_info():
    """Ask the instance metadata service (IMDSv2) who we are. Cached once it works."""
    global last_try
    if info or time.time() - last_try < 30:
        return
    last_try = time.time()
    try:
        req = urllib.request.Request(f"{IMDS}/api/token", method="PUT",
                                     headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"})
        token = urllib.request.urlopen(req, timeout=1).read().decode()
        info.update({
            "host": metadata("local-hostname", token).split(".")[0],
            "az": metadata("placement/availability-zone", token),
            "ip": metadata("local-ipv4", token),
            "id": metadata("instance-id", token),
            "type": metadata("instance-type", token),
        })
    except Exception:
        pass  # not on EC2, or metadata not reachable yet


def uptime():
    mins = int(time.time() - STARTED) // 60
    return f"{mins // 60}h {mins % 60}m" if mins >= 60 else f"{mins}m"


def page():
    host = info.get("host", gethostname())
    az = info.get("az", "not on EC2")
    colour = AZ_COLOURS.get(az[-1:], "#8FA0BD")
    rows = [
        ("Availability Zone", az),
        ("private IP", info.get("ip", "unknown")),
        ("instance", info.get("id", "unknown")),
        ("instance type", info.get("type", "unknown")),
        ("requests served", str(served)),
        ("running for", uptime()),
    ]
    cells = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hello from {host}</title>
<style>
  :root {{ --az: {colour}; }}
  body {{ margin: 0; min-height: 100vh; display: grid; place-items: center;
         background: #0C1220; color: #C7D0E8;
         font-family: ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace; }}
  main {{ border: 1.5px solid var(--az); border-radius: 14px; padding: 32px 36px;
          max-width: 560px; width: calc(100% - 48px); box-sizing: border-box;
          background: #141E2C; }}
  p {{ margin: 0 0 6px; color: #5B7290; font-size: 14px; }}
  h1 {{ margin: 0 0 24px; font-size: clamp(22px, 5vw, 32px); font-weight: 600;
        color: var(--az); overflow-wrap: anywhere; }}
  dl {{ display: grid; grid-template-columns: auto 1fr; gap: 10px 24px; margin: 0; font-size: 14px; }}
  dt {{ color: #5B7290; }}
  dd {{ margin: 0; color: #E6EBF5; overflow-wrap: anywhere; }}
  footer {{ margin-top: 24px; font-size: 12px; color: #3D5170; }}
</style></head>
<body><main>
  <p>Hello from</p>
  <h1>{host}</h1>
  <dl>{cells}</dl>
  <footer>inthelab test server, served {datetime.now(timezone.utc):%H:%M:%S} UTC</footer>
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global served
        served += 1
        load_info()
        if "curl" in self.headers.get("User-Agent", ""):
            # plain text for the terminal
            body = (f"Hello from {info.get('host', gethostname())} "
                    f"({info.get('az', 'not on EC2')})\n").encode()
            ctype = "text/plain; charset=utf-8"
        else:
            body = page().encode()
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # one short line per request, visible with: journalctl -u hello
        print(f"{self.client_address[0]} {self.command} {self.path}", flush=True)


if __name__ == "__main__":
    load_info()
    print(f"hello-server listening on port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()