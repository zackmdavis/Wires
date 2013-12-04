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
        self.validations.append(self.validate_email)
        self.validate_presence_of("author")
        self.validate_presence_of("email")
        self.validate_presence_of("body")

    def validate_presence_of(self, attribute_name):
        def validate_attribute():
            try:
                attribute = getattr(self, attribute_name)
                if attribute:
                    return None
            except AttributeError:
                pass
            return "{0} can't be blank".format(attribute_name)
        self.validations.append(validate_attribute)

    def validate_email(self):
        if "@" not in self.email:
            return "invalid email address"
