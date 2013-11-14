from wires import *

from models.post import Post
from models.user import User

from hashlib import sha1

def new(parameters):
    template = open('./templates/sessions/new.html').read()
    return TemplateEngine(template, parameters).render()

def login(parameters):
    user = User.find_where(User.cxn, "users", {"username": parameters["username"]})
    if not user:
        return False
    if user.authenticate(parameters["password"]):
        session_token = user.set_session_token()
        user.save()
        return session_token
    else:
        return False

def logout(parameters):
    user = User.find_where(User.cxn, "users", {"session_token": parameters["session_token"]})
    if user:
        user.session_token = ''
        user.save()
        return True
    else:
        return False
