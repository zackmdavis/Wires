import sqlite3
from pdb import set_trace as debug

class MassObject:
    def __init__(self, attributes):
        for name, value in attributes.items():
            setattr(self, name, value)

class SqlObject(MassObject):
    def __init__(self, db_connection, table_name, attributes = {}, id = None):
        super().__init__(attributes)
        self.table_name = table_name
        self.id = id
        self.db_connection = db_connection
        self.db_connection.row_factory = sqlite3.Row
        self.cursor = db_connection.cursor()

    @property
    def attributes(self):
        attr_dict = self.__dict__.copy()
        del attr_dict['table_name']
        del attr_dict['db_connection']
        del attr_dict['cursor']
        del attr_dict['id']
        return attr_dict

    def __repr__(self):
        return "<{0} {1} {2}>".format(self.table_name, self.id, str(self.attributes)[1:-1])

    @classmethod
    def all(cls, db_connection, table_name):
        query = "SELECT * FROM {0};".format(table_name)
        results = db_connection.execute(query).fetchall()
        result_dicts = [cls.dict_from_row(row) for row in results]
        return [SqlObject(db_connection, table_name, rd, rd["id"]) for rd in result_dicts]

    @classmethod
    def find(cls, db_connection, table_name, id):
        query = "SELECT * FROM {0} WHERE id = ?;".format(table_name)
        result = db_connection.execute(query, (id,)).fetchone()
        result_dict = cls.dict_from_row(result)
        return SqlObject(db_connection, table_name, result_dict, id)

    @classmethod
    def where(cls, db_connection, table_name, search_parameters):
        where_string = ["{0} = ?".format(k) for k in search_parameters]
        where_string = ", ".join(where_string)
        query = "SELECT * FROM {0} WHERE {1}".format(table_name, where_string)
        results = db_connection.execute(query, tuple(search_parameters.values())).fetchall()
        result_dicts = [cls.dict_from_row(row) for row in results]
        return [SqlObject(db_connection, table_name, rd, rd["id"]) for rd in result_dicts]

    @staticmethod
    def question_marks(n):
        if n == 1:
            return "?"
        else:
            marks_string = "("
            for _ in range(n-1):
                marks_string += "?, "
            marks_string += "?)"
            return marks_string

    @staticmethod
    def dict_from_row(row):
        row_dict = {}
        for key in row.keys():
            row_dict[key] = row[key]
        return row_dict

    def create(self):
        attribute_names, attribute_values = zip(*self.attributes.items())
        query = "INSERT INTO {0} {1} VALUES {2};".format(self.table_name, attribute_names, SqlObject.question_marks(len(attribute_values)))
        self.cursor.execute(query, attribute_values)
        self.db_connection.commit()
        self.id = self.cursor.lastrowid
        return self.id

    def update(self):
        set_string = ["{0} = ?".format(k) for k in self.attributes]
        set_string = ", ".join(set_string)
        query = "UPDATE {0} SET {1} WHERE id = ?".format(self.table_name, set_string)
        self.cursor.execute(query, tuple(self.attributes.values())+(self.id,))
        self.db_connection.commit()

    def save(self):
        if self.id is None:
            self.create()
        else:
            self.update()
