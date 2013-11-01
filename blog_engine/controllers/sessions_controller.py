from wires import *

from models.post import Post
from models.user import User

from hashlib import sha1

class SessionsController:

    def new(parameters):
        template = open('./views/sessions/new.html').read()
        return TemplateEngine(template, parameters).render()

    def login(parameters):
        user = User.where(User.cxn, "users", {"username": parameters["username"]})[0]
        if user.authenticate(parameters["password"]):
            session_token = user.set_session_token()
            user.save()
            return session_token
        else:
            return False

    def logout(parameters):
        user = User.where(user.cxn, "users", {"session_token": parameters["session_token"]})
        user.session_token = ''
        return True
