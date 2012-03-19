#!/usr/bin/env python

import SocketServer
import urllib
import sys

from SimpleHTTPServer import SimpleHTTPRequestHandler

PORT = 8080

URI_PREFIX = ""
CSS_FILE = ""

CSS_SWAP_ONCE_MUTEX = []

FILTER_PATHS = ["/resources", "/external", "/js"]

class CSSProxy(SimpleHTTPRequestHandler):

    def filter_path(self):
        return any([self.path.startswith(p) for p in FILTER_PATHS])

    def do_GET(self):
        if self.path == "/":
            CSS_SWAP_ONCE_MUTEX.append(True)

        if self.filter_path():
            self.not_found()
            return


        if self.path.split("?", 1)[0].endswith(".css"):
            if not len(CSS_SWAP_ONCE_MUTEX):
                self.not_found()
                return

            CSS_SWAP_ONCE_MUTEX.pop()

            self.path = "/%s" % CSS_FILE
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
        else:
            url = URI_PREFIX + self.path
            f = urllib.urlopen(url)
            if f:
                self.copyfile(f, self.wfile)
                f.close()

    def not_found(self):
        self.send_response(404, "File not found")
        self.send_header("Content-Type", self.error_content_type)
        self.send_header('Connection', 'close')
        self.end_headers()

    def log_request(self, code='-', size='-'):
        self.log_message('"%s" %s %s',
                         "GET %s" % self.path, str(code), str(size))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s <uri> <css>\n' % sys.argv[0])
        sys.exit(1)

    URI_PREFIX = sys.argv[1]
    CSS_FILE = sys.argv[2]

    try:
        httpd = ThreadedTCPServer(("", PORT), CSSProxy)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
        httpd.shutdown()
