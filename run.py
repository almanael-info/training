#!/usr/bin/python3

from http.server import HTTPServer, SimpleHTTPRequestHandler


class Handler(SimpleHTTPRequestHandler):
    def do_HEAD(self) -> None:
        if self.path == '/':
            self.path = '/index.html'
        return super().do_HEAD()

    def do_GET(self) -> None:
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()


def run_server():
    http = HTTPServer(("0.0.0.0", 8000), Handler)
    http.serve_forever()


if __name__ == "__main__":
    run_server()
