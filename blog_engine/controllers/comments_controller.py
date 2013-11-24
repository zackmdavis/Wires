from wires import *

from models.post import Post
from models.comment import Comment

def create(parameters):
    comment = Comment(Comment.cxn, "comments", parameters)
    try:
        comment.save()
        return '["Comment saved!"]'
    except:
        return '["Comment could not be saved!"]'

