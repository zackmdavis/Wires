from wires import *

from models.user import User

class UsersController:

    def new(parameters):
        template = open('./views/users/new.html').read()
        definitions = {}
        return TemplateEngine(template, definitions).render()

    def create(parameters):
        pass # TODO
        # user.__init__ method signature--
        # (self, username, display_name, password, confirm_password):

