from sys import path
path.append('../wires')

from server import run_server

from request_handler import RequestHandler
import re
RequestHandler.get[re.compile("^/posts$")] = ("Posts", "index")
RequestHandler.get[re.compile("^/posts/(?P<id>\d+)$")] = ("Posts", "show")

from controllers import *

if __name__ == '__main__':
    run_server('localhost', 8080, RequestHandler)
