from wires import *

from models.post import Post
from models.user import User

from hashlib import sha1

def new(parameters):
    template = open('./views/sessions/new.html').read()
    return TemplateEngine(template, parameters).render()

def login(parameters):
    try:
        user = User.where(User.cxn, "users", {"username": parameters["username"]})[0]
    # if no such user exists, we get an empty list, no index of which
    # is in range
    except IndexError:
        return False
    if user.authenticate(parameters["password"]):
        session_token = user.set_session_token()
        user.save()
        return session_token
    else:
        return False

def logout(parameters):
    try:
        user = User.where(User.cxn, "users", {"session_token": parameters["session_token"]})[0]
    # if no such user exists, we get an empty list, no index of which
    # is in range
    except IndexError:
        return False
    user.session_token = ''
    user.save()
    return True
