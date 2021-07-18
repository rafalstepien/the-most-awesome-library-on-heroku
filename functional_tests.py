from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class UserBehaviorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_user_adds_book_and_finds_it_in_the_table(self):
        # User enters the all boks page and is able to see table with current
        # books
        self.browser.get('http://127.0.0.1:8000/all_books/')
        table = self.browser.find_element_by_tag_name('tr').text
        self.assertIn('ID', table)
        self.assertIn('Title', table)
        self.assertIn('Author', table)

        # User adds his favorite book to the database
        self.browser.get('http://127.0.0.1:8000/add_book/')
        title_inputbox = self.browser.find_element_by_id('id_title')
        title_inputbox.send_keys('Harry Potter and The Goblet of Fire')

        author_inputbox = self.browser.find_element_by_id('id_author')
        author_inputbox.send_keys('J.K. Rowling')

        language_inputbox = self.browser.find_element_by_id('id_language')
        language_inputbox.send_keys('en')

        author_inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(10)

        # User navigates to all books view page
        self.browser.get('http://127.0.0.1:8000/all_books/')

        # User finds his book in the database
        table = self.browser.find_element_by_tag_name('tbody').text
        self.assertIn('Harry Potter and The Goblet of Fire', table)

    def test_user_filters_books_by_author_and_title(self):
        pass

    def test_user_editing_existing_book(self):
        pass

    def test_user_editing_existing_book(self):
        pass

    def test_user_adding_books_by_keywords(self):
        pass
