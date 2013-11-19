import sqlite3
from subprocess import call

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os, binascii

class TestLinks(unittest.TestCase):

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

class TestAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    def setUp(self):
        self.driver.get("http://localhost:8080/")

    def log_in(self):
        self.driver.find_element_by_id("login_link").click()
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys("admin")
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("admin")
        self.driver.find_element_by_id("login_submit").click()

    def log_out(self):
        self.driver.find_element_by_id("logout_link").click()

    def test_sign_in_and_out(self):
        # shouldn't be logged in to start with
        auth_msg = self.driver.find_element_by_id("authentication_status").text
        self.assertIn("not logged in", auth_msg)

        # should be able to log in
        self.log_in()
        auth_msg = self.driver.find_element_by_id("authentication_status").text
        self.assertIn("logged in as Administrator (admin)", auth_msg)
        
        # should be able to log out
        self.log_out()
        auth_msg = self.driver.find_element_by_id("authentication_status").text
        self.assertIn("not logged in", auth_msg)

    def test_can_sign_in_and_post(self):
        self.log_in()
        self.driver.find_element_by_id("new_post_link").click()
        stamp = str(binascii.b2a_hex(os.urandom(4)), encoding="utf-8")
        title = "Test Post " + stamp
        body = "This is the body of {0}.".format(title)
        title_field = self.driver.find_element_by_id("title")
        title_field.send_keys(title)
        body_field = self.driver.find_element_by_id("body")
        body_field.send_keys(body)
        author_id_field = self.driver.find_element_by_id("author_id")
        author_id_field.send_keys("1")
        self.driver.find_element_by_id("new_post_submit").click()
        page = self.driver.page_source
        self.assertIn(stamp, page)
        self.log_out()

    # not yet implemented
    def test_cannot_post_if_not_logged_in(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        

if __name__ == '__main__':
    unittest.main()
