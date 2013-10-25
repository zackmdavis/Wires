from wires import *

from models.post import Post

class PostsController:

    # Note the curious absence of "self" in the methods below!---these methods
    # are "plucked" from this class and included as values in the routing
    # dictionaries of the request handler.

    def index(parameters):
        template = open('./views/posts/index.html').read()
        posts = Post.all(Post.cxn, "posts")
        post_template = open('./views/posts/show.html').read()
        rendered_posts = "<br><br>".join([TemplateEngine(post_template, PostsController.definitions(post, {"id":post.id})).render() for post in posts])
        return TemplateEngine(template, {"rendered_posts": rendered_posts}).render()

    def show(parameters):
        post = Post.find(Post.cxn, "posts", parameters["id"])
        template = open('./views/posts/show.html').read()
        return TemplateEngine(template, PostsController.definitions(post, parameters)).render()

    def new(parameters):
        template = open('./views/posts/new.html').read()
        definitions = {}
        return TemplateEngine(template, definitions).render()

    def create(parameters):
        new_post = Post(parameters["title"], parameters["author_id"], parameters["body"])
        new_post.save()
        return PostsController.show({"id": str(new_post.id)})

    # helper method for construction substitution definitions from supplied
    # object and request parameters
    def definitions(post, parameters):
        defns_dict = dict(list(parameters.items()) + list(post.attributes.items()))
        return {key: str(defns_dict[key]) for key in defns_dict}