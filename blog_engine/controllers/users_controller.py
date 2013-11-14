from wires import *

from models.user import User
from models.post import Post

from hashlib import sha1

def new(parameters):
    template = open('./templates/users/new.html').read()
    return TemplateEngine(template, parameters).render()

def create(parameters):
    if parameters["password"] == parameters["confirm_password"]:
        parameters["password_digest"] = sha1(bytes(parameters["password"], 'utf-8')).hexdigest()
        user = User(User.cxn, "users", parameters)
        user.save()
        return "<html><head></head><body><h2>{0}</h2>{1}</body></html>".format("User created!", "<a href='/'><em>(home)</em></a>")
    else:
        return "<html><head></head><body><h2>{0}</h2>{1}</body></html>".format("password confirmation doesn't match", "<a href='/'><em>(home)</em></a>")

def show(parameters):
    user = User.find(User.cxn, "users", parameters["id"])
    template = open('./templates/users/show.html').read()
    definitions = parameters.copy()
    posts = user.posts(globals())
    post_display_list = "<ul>" + ''.join(['<li><a href="/posts/{0}">{1}</a></li>'.format(post.id, post.title)
                         for post in posts]) + "</ul>"
    definitions.update({"display_name": user.display_name,
                        "username": user.username,
                        "post_display_list": post_display_list})
    return TemplateEngine(template, definitions).render()