from wires import *

from models.user import User

def new(parameters):
    template = open('./views/users/new.html').read()
    return TemplateEngine(template, parameters).render()

def create(parameters):
    pass # TODO
    # user.__init__ method signature--
    # (self, username, display_name, password, confirm_password):
