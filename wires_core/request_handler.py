import http.server

from collections import OrderedDict

from urllib.parse import parse_qs

from http.cookies import SimpleCookie

class RequestHandler(http.server.BaseHTTPRequestHandler):

    get = OrderedDict()
    post = OrderedDict()
    put = OrderedDict()
    delete = OrderedDict()

    @staticmethod
    def full_action(path, routes):
        action, parameters = None, {}
        for route in routes.keys():
            match = route.match(path)
            if match:
                action = routes[route]
                parameters = match.groupdict()
                break
        return (action, parameters)

    def dictionary_from_cookie(self):
        cookie = SimpleCookie()
        if self.headers.get('Cookie'):
            cookie.load(self.headers.get('Cookie'))
            cookie_parameters = {key: cookie[key].value for key in cookie}
            for key in cookie_parameters:
                try:
                    cookie_parameters[key] = int(cookie_parameters[key])
                except ValueError:
                    pass
            return cookie_parameters
        else:
            return {}

    def set_cookie_from_dictionary(self, cookie_parameters):
        cookie = SimpleCookie(cookie_parameters)
        for key in cookie:
            cookie[key]['path'] = '/'
            self.send_header("Set-Cookie", cookie[key].OutputString())

    def return_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = "<html><head></head><body><h2>{0}</h2></body></html>".format(message)
        self.wfile.write(bytes(page, 'UTF-8'))

    def return_success(self, page, cookie_parameters):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.set_cookie_from_dictionary(cookie_parameters)
        self.end_headers()
        self.wfile.write(bytes(page, 'UTF-8'))

    def do_GET(self):
        action, parameters = RequestHandler.full_action(self.path, self.get)
        parameters.update(self.dictionary_from_cookie())
        cookie_keys = ["session_token", "number_of_pages"]
        cookie_parameters = {key: parameters[key] for key in parameters if key in cookie_keys}
        try:
            cookie_parameters["number_of_pages"] += 1
        except KeyError:
            cookie_parameters["number_of_pages"] = 1
        parameters.update(cookie_parameters)
        if action:
            if action.__name__ == "logout":
                # this despite the admitted fact one could make a very
                # strong case that logging out should be done with a
                # DELETE request---or possibly POST, but in any case
                # certainly not GET!
                action(parameters)
                cookie_parameters["session_token"] = "loggedout"
                page = "<html><head></head><body><h2>{0}</h2>{1}</body></html>".format("Successfully logged out!", "<a href='/posts'><em>(home)</em></a>")
            else:
                page = action(parameters)
            self.return_success(page, cookie_parameters)
        else:
            self.return_error(404, "Not Found")

    def do_POST(self):
        action, parameters = RequestHandler.full_action(self.path, self.post)
        parameters.update(self.dictionary_from_cookie())
        if action:
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            raw_body_parameters = parse_qs(body)
            body_parameters = {key.decode('utf-8'): raw_body_parameters[key][0].decode('utf-8') for key in raw_body_parameters}
            parameters.update(body_parameters)
            if action.__name__ == "login":
                session_token = action(parameters)
                if session_token:
                    parameters["session_token"] = session_token
                    page = "<html><head></head><body><h2>{0}</h2>{1}</body></html>".format("Successfully logged in!", "<a href='/posts'><em>(home)</em></a>")
                else:
                    page = "<html><head></head><body><h2>{0}</h2></body></html>".format("Invalid credentials")
            else:
                page = action(parameters)
            cookie_keys = ["session_token", "number_of_pages"]
            cookie_parameters = {key: parameters[key] for key in parameters if key in cookie_keys}
            self.return_success(page, cookie_parameters)
        else:
            self.return_error(500, "Internal Server Error")
