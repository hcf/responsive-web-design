#!/usr/bin/env python
#
# Usage: http://localhost:40808/?swap_css=<local.css>
#

import SocketServer
import urllib
import sys

from SimpleHTTPServer import SimpleHTTPRequestHandler

PORT = 8080

URI_PREFIX = ""
CSS_FILE = ""

FILTER_PATHS = ["/resources", "/external", "/js"]

class CSSProxy(SimpleHTTPRequestHandler):

    def filter_path(self):
        return any([self.path.startswith(p) for p in FILTER_PATHS])

    def do_GET(self):
        if self.filter_path():
            self.send_response(404, "File not found")
            self.send_header("Content-Type", self.error_content_type)
            self.send_header('Connection', 'close')
            self.end_headers()
            return


        if self.path.endswith(".css"):
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
