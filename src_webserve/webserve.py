# src/webserve.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import html

def get_handler(endpoints):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:

                path = urlparse(self.path).path
                renderer = endpoints.get(path,None)

                if not renderer:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")
                    return

                content, conent_type = renderer(self.path)
                if not conent_type:
                    conent_type = 'text/html'

                self.send_response(200)
                self.send_header(f"Content-type", f"{conent_type}; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(html.escape(str(e)).encode())
    return Handler


def run(address='0.0.0.0',port_num=8051,endpoints=None):
    if endpoints is None:
        endpoints = {}
    server = HTTPServer((address, port_num), get_handler(endpoints))
    server.serve_forever()
