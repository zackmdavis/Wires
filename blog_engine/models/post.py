import os

from sys import path
path.append('../..')
path.append('.')
path.append('models')
from wires import *

import sqlite3

class Post(SqlObject):

    cxn = sqlite3.connect('./database.db')
    cxn.row_factory = sqlite3.Row

    table_name = "posts"

    def __init__(self, db_connection, table_name, attributes = {}, id = None):
        attributes = {attribute: attributes[attribute] for attribute in attributes
                      if attribute in ("title", "body", "author_id")}
        super().__init__(self.cxn, "posts", attributes, id)
        self.belongs_to("author", "User", "author_id")

