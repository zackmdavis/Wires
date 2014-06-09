import unittest
import sqlite3
from subprocess import call

from sys import path
path.append('../serpentine_record')

from serpentine_record import SqlObject

class TestStaticMethods(unittest.TestCase):

    def test_query_parameterization(self):
        self.assertEqual("?", SqlObject.question_marks(1))
        self.assertEqual("(?, ?, ?)", SqlObject.question_marks(3))


class TestSqlObject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        call('./refresh_test_database.bash')
        cls.cxn = sqlite3.connect('test_database.db')
        initialize_query = '''CREATE TABLE test_items(
                              id INTEGER PRIMARY KEY,
                              attribute1 INTEGER,
                              attribute2 VARCHAR(20));'''
        cls.cxn.execute(initialize_query)

    def setUp(self):
        self.our_sql_object = SqlObject(self.cxn, "test_items", {'attribute1': 1, 'attribute2': "friendship"})

    def testCreation(self):
        self.our_sql_object.save()
        retrieved_sql_object = SqlObject.find(self.cxn, "test_items", self.our_sql_object.id)
        self.assertEqual(self.our_sql_object.attribute1, retrieved_sql_object.attribute1)
        self.assertEqual(self.our_sql_object.attribute2, retrieved_sql_object.attribute2)
        self.assertEqual(self.our_sql_object.id, retrieved_sql_object.id)

    def testAttributeUpdating(self):
        self.our_sql_object.attribute2 = "alliance"
        self.assertEqual(self.our_sql_object.attributes["attribute2"], "alliance")

    def testUpdating(self):
        self.our_sql_object.save()
        self.our_sql_object.attribute2 = "rivalry"
        self.our_sql_object.save()
        retrieved_sql_object = SqlObject.find(self.cxn, "test_items", self.our_sql_object.id)
        self.assertEqual(retrieved_sql_object.attribute2, self.our_sql_object.attribute2)

    def testWhere(self):
        sql_object_where = SqlObject(self.cxn, "test_items", {'attribute1': 45, 'attribute2': "coffee"})
        sql_object_where.save()
        retrieved_objects_where = SqlObject.where(self.cxn, "test_items", {'attribute2': "coffee"})
        self.assertEqual(len(retrieved_objects_where), 1)
        self.assertEqual(retrieved_objects_where[0].id, sql_object_where.id)

if __name__ == '__main__':
    unittest.main()
