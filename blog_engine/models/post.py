import os

from sys import path
path.append('../..')
from wires import *

import sqlite3

class Post(SqlObject):

    cxn = sqlite3.connect('./database.db')
    cxn.row_factory = sqlite3.Row

    def __init__(self, db_connection, table_name, attributes = {}, id = None):
        attributes = {attribute: attributes[attribute] for attribute in attributes
                      if attribute in ("title", "body", "author_id")}
        super().__init__(self.cxn, "posts", attributes, id)

