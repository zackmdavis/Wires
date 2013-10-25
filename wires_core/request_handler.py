import http.server

from collections import OrderedDict

from urllib.parse import parse_qs

class RequestHandler(http.server.BaseHTTPRequestHandler):

    get = OrderedDict()
    post = OrderedDict()
    put = OrderedDict()
    delete = OrderedDict()

    @staticmethod
    def full_action(path, routes):
        action, parameters = None, None
        for route in routes.keys():
            match = route.match(path)
            if match:
                action = routes[route]
                parameters = match.groupdict()
                break
        return (action, parameters)

    def return_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = "<html><head></head><body><h2>{0}</h2></body></html>".format(message)
        self.wfile.write(bytes(page, 'UTF-8'))

    def return_success(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page, 'UTF-8'))

    def do_GET(self):
        action, parameters = RequestHandler.full_action(self.path, self.get)
        if action:
            page = action(parameters)
            self.return_success(page)
        else:
            self.return_error(404, "Not Found")

    def do_POST(self):
        action, parameters = RequestHandler.full_action(self.path, self.post)
        if action:
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            raw_body_parameters = parse_qs(body)
            body_parameters = {key.decode('utf-8'): raw_body_parameters[key][0].decode('utf-8') for key in raw_body_parameters}
            parameters.update(body_parameters)
            page = action(parameters)
            self.return_success(page)
        else:
            self.return_error(500, "Internal Server Error")
