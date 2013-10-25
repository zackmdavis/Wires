from wires import *

from models.post import Post

class PostsController:

    def index(parameters):
        template = open('./views/index.html').read()
        return TemplateEngine(template, parameters).render()

    def show(parameters):
        post = Post.find(Post.cxn, "posts", parameters["id"])
        template = open('./views/show.html').read()
        attributes = {key:str(post.attributes[key]) for key in post.attributes}
        definitions = dict(list(parameters.items()) + list(attributes.items()))
        return TemplateEngine(template, definitions).render()

    def new(parameters):
        template = open('./views/new.html').read()
        definitions = {}
        return TemplateEngine(template, definitions).render()

    def create(parameters):
        pass