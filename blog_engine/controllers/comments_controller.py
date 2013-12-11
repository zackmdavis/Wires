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
    except ValidationError as ve:
        response = {"status": 422, "errors": ve.messages}
        return json.dumps(response)
    except Exception as e:
        print(str(e))
        response = {"status": 500, "errors": [str(e)]}
        return json.dumps(response)
