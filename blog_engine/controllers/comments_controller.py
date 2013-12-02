from wires import *

from models.post import Post
from models.comment import Comment

import json

def create(parameters):
    comment = Comment(Comment.cxn, "comments", parameters)
    try:
        comment.save()
        attributes_to_render = comment.attributes
        attributes_to_render.update({"id": comment.id})
        template = open('./templates/comments/show.html').read()
        attributes_to_render.update({"html": TemplateEngine(template, attributes_to_render).render_partial()})
        return json.dumps(attributes_to_render)
    # Even though these are intended as errors, they're still being
    # sent back as an HTTP 200 OK. It's important to fix this so that
    # the jQuery can use a separate error callback.
    except ValidationError as ve:
        return json.dumps(ve.messages)
    except:
        return '["An error occurred!"]'
