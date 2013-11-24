import os

from sys import path
path.append('../..')
from wires import *

import sqlite3

class Comment(SqlObject):

    cxn = sqlite3.connect('./database.db')
    cxn.row_factory = sqlite3.Row

    table_name = "comments"

    def __init__(self, db_connection, table_name, attributes = {}, id = None):
        attributes = {attribute: attributes[attribute] for attribute in attributes
                      if attribute in ("author", "email", "website", "body", "post_id")}
        super().__init__(self.cxn, "comments", attributes, id)
        self.belongs_to("post", "Post", "post_id")
