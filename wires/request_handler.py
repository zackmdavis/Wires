import http.server

from collections import OrderedDict

# from sys import path
# path.append('../demo/controllers')
#
# from controllers import PostsController

# from ..demo.controllers import PostsController

# Scaffolding hack because apparently I don't understand how relative imports
# work
class PostsController:

    def index(parameters):
        return '''<html><head><title>Testing Title</title></head>
        <body><h2>Posts</h2><p>I'm in the posts controller!</p></body>
        </html>'''

    def show(parameters):
        return '''<html><head><title>Testing Title</title></head>
        <body><h2>Posts</h2><p>You've requested post #{0}</p></body>
        </html>'''.format(parameters["id"])

class RequestHandler(http.server.BaseHTTPRequestHandler):

    get = OrderedDict()
    post = OrderedDict()
    put = OrderedDict()
    delete = OrderedDict()

    def do_GET(self):
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

    def do_POST(self):
        pass
