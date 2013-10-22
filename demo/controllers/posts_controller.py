from sys import path
path.append('../../wires')

from template_engine import TemplateEngine

class PostsController:

    def index(parameters):
        template = open('./views/index.html').read()
        return TemplateEngine(template, parameters).render()

    def show(parameters):
        template = open('./views/show.html').read()
        return TemplateEngine(template, parameters).render()
