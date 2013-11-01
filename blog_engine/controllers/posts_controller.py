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
        rendered_posts = "<br><br>".join([TemplateEngine(post_template,
                                         PostsController.definitions(post, {"id":post.id})).render_partial()
                                         for post in posts])
        index_definitions = {"number_of_pages": str(parameters["number_of_pages"]), "rendered_posts": rendered_posts}
        return TemplateEngine(template, index_definitions).render()

    def show(parameters):
        post = Post.find(Post.cxn, "posts", parameters["id"])
        template = open('./views/posts/show.html').read()
        return TemplateEngine(template, PostsController.definitions(post, parameters)).render()

    def new(parameters):
        template = open('./views/posts/new.html').read()
        return TemplateEngine(template, parameters).render()

    def create(parameters):
        parameters["body"] = parameters["body"].replace("\n", "<br>")
        new_post = Post(Post.cxn, "posts", parameters)
        new_post.save()
        parameters.update({"id": str(new_post.id)})
        return PostsController.show(parameters)

    # helper method for construction substitution definitions from supplied
    # object and request parameters
    def definitions(post, parameters):
        defns_dict = dict(list(parameters.items()) + list(post.attributes.items()))
        return {key: str(defns_dict[key]) for key in defns_dict}