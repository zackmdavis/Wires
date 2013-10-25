import http.server

from collections import OrderedDict

class RequestHandler(http.server.BaseHTTPRequestHandler):

    get = OrderedDict()
    post = OrderedDict()
    put = OrderedDict()
    delete = OrderedDict()

    def do_GET(self):
        action = None
        for route in self.get.keys():
            match = route.match(self.path)
            if match:
                action = self.get[route]
                parameters = match.groupdict()
                break
        if action:
            page = action(parameters)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(page, 'UTF-8'))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            page = "<html><head></head><body><h3>not found</h3></body></html>"
            self.wfile.write(bytes(page, 'UTF-8'))

    def do_POST(self):
        page = "<html><head></head><body><h3>not yet implemented</h3></body></html>"
        self.wfile.write(bytes(page, 'UTF-8'))
