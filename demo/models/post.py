import os

from sys import path
path.append('../..')
from wires import *

import sqlite3

class Post(SqlObject):

    cxn = sqlite3.connect('./demo_database.db')
    cxn.row_factory = sqlite3.Row

    def __init__(self, title, author_id, body):
        super().__init__(self.cxn, "posts", {"title": title, "author_id": author_id, "body": body})

