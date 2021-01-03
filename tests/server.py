#!/usr/bin/env python3
import http.server
import socketserver

PORT = 8086
DIR = 'sre'

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server, directory=DIR)
        self.extensions_map = {
            '': 'application/octet-stream',
            '.manifest': 'text/cache-manifest',
            '.html': 'text/html',
            '.png': 'image/png',
            '.jpg': 'image/jpg',
            '.svg':	'image/svg+xml',
            '.css':	'text/css',
            '.js':'application/x-javascript',
            '.wasm': 'application/wasm',
            '.json': 'application/json',
            '.xml': 'application/xml',
        }

with socketserver.TCPServer(("localhost", PORT), HttpRequestHandler) as httpd:
    try:
        print(f"serving at http://localhost:{PORT}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass