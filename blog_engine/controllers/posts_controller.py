from wires import *

from models.post import Post

class PostsController:

    # Note the curious absence of "self" in the methods below!---these methods
    # are "plucked" from this class and included as values in the routing
    # dictionaries of the request handler.

    def index(parameters):
        template = open('./views/posts/index.html').read()
        return TemplateEngine(template, parameters).render()

    def show(parameters):
        post = Post.find(Post.cxn, "posts", parameters["id"])
        template = open('./views/posts/show.html').read()
        attributes = {key:str(post.attributes[key]) for key in post.attributes}
        definitions = dict(list(parameters.items()) + list(attributes.items()))
        return TemplateEngine(template, definitions).render()

    def new(parameters):
        template = open('./views/posts/new.html').read()
        definitions = {}
        return TemplateEngine(template, definitions).render()

    def create(parameters):
        new_post = Post(parameters["title"], parameters["author_id"], parameters["body"])
        new_post.save()
        return PostsController.show({"id": str(new_post.id)})