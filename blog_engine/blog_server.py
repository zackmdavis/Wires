from sys import path
path.append('..')
from wires import *

from controllers.posts_controller import *

import re

from pdb import set_trace as debug

RequestHandler.get[re.compile("^/posts$")] = PostsController.index
RequestHandler.get[re.compile("^/posts/(?P<id>\d+)$")] = PostsController.show
RequestHandler.get[re.compile("^/posts/new$")] = PostsController.new
RequestHandler.post[re.compile("^/posts$")] = PostsController.create

if __name__ == '__main__':
    run_server('localhost', 8080, RequestHandler)
