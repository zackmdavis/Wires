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

    def __init__(self, username, display_name, password_digest, session_token):
        super().__init__(self.cxn, "users", {"username": username,
                                             "display_name": display_name,
                                             "password_digest": password_digest,
                                             "session_token": session_token})

    @classmethod
    def where(cls, db_connection, table_name, search_parameters):
        parent_where = super().where(db_connection, table_name, search_parameters)[0]
        return User(parent_where.username, parent_where.display_name,
                    parent_where.password_digest, parent_where.session_token)

    def set_session_token(self):
        self.session_token = sha1(bytes(self.username + str(time()), 'utf-8')).hexdigest()
        return self.session_token

    def authenticate(self, password):
        if sha1(bytes(password, 'utf-8')).hexdigest() == self.password_digest:
            return True
        else:
            return False
