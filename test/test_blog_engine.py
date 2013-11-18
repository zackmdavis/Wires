import sqlite3
from subprocess import call

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from sys import path
path.append('../')

class TestBlogEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # In the future, there should be any easy way to run the blog
        # server with a separate test database. When that becomes the
        # case, use the following to set up the test database (and
        # edit tests accordingly).

        # call('./refresh_test_database.bash')
        # cls.cxn = sqlite3.connect('test_database.db')
        # initialize_query = '''
        #     CREATE TABLE posts(
        #          id INTEGER PRIMARY KEY,
        #          title VARCHAR(100),
        #          author_id INTEGER,
        #          body TEXT);

        #     CREATE TABLE users (
        #          id INTEGER PRIMARY KEY,
        #          username VARCHAR(30),
        #          display_name VARCHAR(60),
        #          password_digest VARCHAR(50),
        #          session_token VARCHAR(50));

        #     INSERT INTO users (id, username, display_name, password_digest, session_token)
        #     VALUES (1, "admin", "Administrator", "d033e22ae348aeb5660fc2140aec35850c4da997", '');

        #     INSERT INTO posts (id, title, body, author_id)
        #     VALUES (1, "Test Post", "<p>This post has been created for use by the automated integration testing system!</p>", 1);
        # '''
        # cls.cxn.executescript(initialize_query)
        cls.driver = webdriver.Firefox()

    def setUp(self):
        self.driver.get("http://localhost:8080/")

    def test_first_post_appears_on_home_page(self):
        page = self.driver.page_source
        self.assertIn("The First Post", page)

    def test_can_click_through_to_first_post(self):
        first_title_link = self.driver.find_element_by_link_text("The First Post")
        first_title_link.click()
        page = self.driver.page_source
        self.assertIn("The First Post", page)
        self.assertNotIn("I Used To Wonder", page)

    def test_can_click_through_to_user_profile(self):
        profile_link = self.driver.find_element_by_link_text("Administrator")
        profile_link.click()
        page = self.driver.page_source
        self.assertIn("The First Post", page)
        self.assertNotIn("I Used To Wonder", page)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == '__main__':
    unittest.main()
