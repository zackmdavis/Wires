from wires import *

from models.user import User
from models.post import Post

def new(parameters):
    template = open('./views/users/new.html').read()
    return TemplateEngine(template, parameters).render()

def create(parameters):
    pass # TODO
    # user.__init__ method signature--
    # (self, username, display_name, password, confirm_password):

def show(parameters):
    user = User.find(User.cxn, "users", parameters["id"])
    template = open('./views/users/show.html').read()
    definitions = parameters.copy()
    posts = user.posts(globals())
    post_display_list = "<ul>" + ''.join(['<li><a href="/posts/{0}">{1}</a></li>'.format(post.id, post.title)
                         for post in posts]) + "</ul>"
    definitions.update({"display_name": user.display_name,
                        "username": user.username,
                        "post_display_list": post_display_list})
    return TemplateEngine(template, definitions).render()