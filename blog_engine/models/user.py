import os

from sys import path
path.append('../..')
from wires import *

import sqlite3

from hashlib import sha1
from time import time

class User(SqlObject):

    cxn = sqlite3.connect('./database.db')
    cxn.row_factory = sqlite3.Row

    table_name = "users"

    def __init__(self, db_connection, table_name, attributes = {}, id = None):
        attributes = {attribute: attributes[attribute] for attribute in attributes
                      if attribute in ("username", "display_name", "password_digest", "session_token")}
        super().__init__(self.cxn, "users", attributes, id)
        self.has_many("posts", "Post", "author_id")

    def set_session_token(self):
        self.session_token = sha1(bytes(self.username + str(time()), 'utf-8')).hexdigest()
        return self.session_token

    def authenticate(self, password):
        if sha1(bytes(password, 'utf-8')).hexdigest() == self.password_digest:
            return True
        else:
            return False
