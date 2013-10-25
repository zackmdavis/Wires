from http.cookies import SimpleCookie

class Session:
    def __init__(self, request):
        if request.headers.get('Cookie'):
            the_cookie = SimpleCookie()
            the_cookie.load(self.headers.get('Cookie'))
            self.session_token = the_cookie['session_token'].value
        else:
            # generate new session token and set in new cookie?
            # or something??