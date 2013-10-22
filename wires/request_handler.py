import http.server

from collections import OrderedDict

from sys import path
path.append('../')

from demo.controllers.posts_controller import *

# don't know how to get this style to work
# from ..demo.controllers.posts_controller import *

class RequestHandler(http.server.BaseHTTPRequestHandler):

    get = OrderedDict()
    post = OrderedDict()
    put = OrderedDict()
    delete = OrderedDict()

    def do_GET(self):
        controller = None
        for route in self.get.keys():
            match = route.match(self.path)
            if match:
                controller, action = self.get[route]
                parameters = match.groupdict()
                break
        if controller:
            page = eval("{0}Controller.{1}({2})".format(controller, action, parameters))
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
        pass
