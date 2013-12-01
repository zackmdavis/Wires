from wires import *

from models.post import Post
from models.user import User
from models.comment import Comment

from pdb import set_trace as debug

def index(parameters):
    template = open('./templates/posts/index.html').read()
    posts = Post.all(Post.cxn, "posts")
    post_template = open('./templates/posts/show.html').read()
    rendered_posts = "<br><br>".join([TemplateEngine(post_template, definitions(post, {"id": post.id, "comments_link": '<p><a href="/posts/{0}#comments">{1} comments</a></p>'.format(post.id, len(post.comments(globals())))})).render_partial() for post in posts])
    index_definitions = {"number_of_pages": str(parameters["number_of_pages"]), "rendered_posts": rendered_posts}
    index_definitions["login_status_message"] = login_status_message(parameters)
    return TemplateEngine(template, index_definitions).render()

def show(parameters):
    post = Post.find(Post.cxn, "posts", parameters["id"])
    template = open('./templates/posts/show.html').read()
    comment_template = open('./templates/comments/show.html').read()    
    show_post_script_tag = '<script src="/show_post.js"></script>'
    comments = post.comments(globals())
    if comments:
        rendered_comments = "<h3>Comments</h3>" + "".join([TemplateEngine(comment_template, comment.attributes).render_partial() for comment in comments])
    else:
        rendered_comments = '<p id="no_comments">No comments yet.</p>'
    new_comment_link_html = '<a id="new_comment_link" href="#">Make a new comment!</a>'
    parameters.update({"rendered_comments": rendered_comments, "new_comment_link": new_comment_link_html, "show_post_script_tag": show_post_script_tag})
    return TemplateEngine(template, definitions(post, parameters)).render()

def new(parameters):
    template = open('./templates/posts/new.html').read()
    return TemplateEngine(template, parameters).render()

def create(parameters):
    parameters["body"] = parameters["body"].replace("\n", "<br>")
    user = current_user(parameters)
    if user:
        parameters.update({"author_id": user.id})
        new_post = Post(Post.cxn, "posts", parameters)
        new_post.save()
        parameters.update({"id": str(new_post.id)})
        return show(parameters)
    else:
        page = "<html><head></head><body><h2>{0}</h2>{1}</body></html>".format("You must be logged in to submit a new post", "<a href='/'><em>(home)</em></a>")
        return page

# helper method for construction substitution definitions from supplied
# object and request parameters
def definitions(post, parameters):
    defns_dict = dict(list(parameters.items()) + list(post.attributes.items()))
    defns_dict["author_display_name"] = post.author(globals()).display_name
    defns_dict["author_id"] = post.author(globals()).id
    return {key: str(defns_dict[key]) for key in defns_dict}

def current_user(parameters):
    if "session_token" in parameters:
        user = User.find_where(User.cxn, "users", {"session_token": parameters["session_token"]})
        return user
    else:
        return None

def login_status_message(parameters):
    user = current_user(parameters)
    if user:
        return "logged in as {0} ({1})".format(user.display_name, user.username)
    return "not logged in"
