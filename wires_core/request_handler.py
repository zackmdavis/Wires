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

    def redirect(self, location, cookie_parameters):
        self.send_response(303)
        self.send_header("Location", location)
        self.set_cookie_from_dictionary(cookie_parameters)
        self.end_headers()

    def return_media(self, file_path, file_type):
        media_file = open(file_path, 'rb').read()
        self.send_response(200)
        self.send_header("Content-type", file_type)
        self.end_headers()
        self.wfile.write(media_file)

    def get_cookie_parameters(self, parameters):
        cookie_keys = ["session_token", "number_of_pages"]
        return {key: parameters[key] for key in parameters if key in cookie_keys}

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.return_media("favicon.ico", "image/ico")
            return
        if self.path == "/application.css":
            self.return_media("templates/layouts/application.css", "text/css")
            return
        if self.path[-3:] == ".js":
            self.return_media("javascripts/" + self.path, "text/javascript")
            return
        action, parameters = RequestHandler.full_action(self.path, self.get)
        parameters.update(self.dictionary_from_cookie())
        cookie_parameters = self.get_cookie_parameters(parameters)
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
                self.redirect("/", cookie_parameters)
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
            cookie_parameters = self.get_cookie_parameters(parameters)
            if action.__name__ == "login":
                session_token = action(parameters)
                if session_token:
                    cookie_parameters["session_token"] = session_token
                    self.redirect("/", cookie_parameters)
                else:
                    page = "<html><head></head><body><h2>{0}</h2>{1}</body></html>".format("Invalid credentials", "<a href='/posts'><em>(home)</em></a>")
                    self.return_success(page, cookie_parameters)
            else:
                page = action(parameters)
                self.return_success(page, cookie_parameters)
        else:
            self.return_error(500, "Internal Server Error")
