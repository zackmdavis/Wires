from wires import *

from models.post import Post
from models.user import User

from pdb import set_trace as debug

def index(parameters):
    template = open('./views/posts/index.html').read()
    posts = Post.all(Post.cxn, "posts")
    post_template = open('./views/posts/show.html').read()
    rendered_posts = "<br><br>".join([TemplateEngine(post_template,
                                     definitions(post, {"id":post.id})).render_partial()
                                     for post in posts])
    index_definitions = {"number_of_pages": str(parameters["number_of_pages"]), "rendered_posts": rendered_posts}
    index_definitions["login_status_message"] = login_status_message(parameters)
    return TemplateEngine(template, index_definitions).render()

def show(parameters):
    post = Post.find(Post.cxn, "posts", parameters["id"])
    template = open('./views/posts/show.html').read()
    return TemplateEngine(template, definitions(post, parameters)).render()

def new(parameters):
    template = open('./views/posts/new.html').read()
    return TemplateEngine(template, parameters).render()

def create(parameters):
    parameters["body"] = parameters["body"].replace("\n", "<br>")
    new_post = Post(Post.cxn, "posts", parameters)
    new_post.save()
    parameters.update({"id": str(new_post.id)})
    return show(parameters)

# helper method for construction substitution definitions from supplied
# object and request parameters
def definitions(post, parameters):
    defns_dict = dict(list(parameters.items()) + list(post.attributes.items()))
    defns_dict["author_display_name"] = post.author(globals()).display_name
    return {key: str(defns_dict[key]) for key in defns_dict}

def login_status_message(parameters):
    if "session_token" in parameters:
        try:
            current_user = User.where(User.cxn, "users", {"session_token": parameters["session_token"]})[0]
            return "logged in as {0} ({1})".format(current_user.display_name, current_user.username)
        except IndexError:
            pass
    return "not logged in"
