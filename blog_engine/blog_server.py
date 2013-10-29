from sys import path
path.append('..')
from wires import *

from controllers.posts_controller import *
from controllers.sessions_controller import *
from controllers.users_controller import *

import re

from pdb import set_trace as debug

RequestHandler.get[re.compile("^/posts$")] = PostsController.index
RequestHandler.get[re.compile("^/posts/(?P<id>\d+)$")] = PostsController.show
RequestHandler.get[re.compile("^/posts/new$")] = PostsController.new
RequestHandler.post[re.compile("^/posts$")] = PostsController.create

RequestHandler.get[re.compile("^/signup$")] = UsersController.new
RequestHandler.post[re.compile("^/signup$")] = UsersController.create

RequestHandler.get[re.compile("^/login$")] = SessionsController.new
RequestHandler.post[re.compile("^/login$")] = SessionsController.login
RequestHandler.delete[re.compile("^/logout$")] = SessionsController.logout

if __name__ == '__main__':
    run_server('localhost', 8080, RequestHandler)
