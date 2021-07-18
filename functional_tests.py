from selenium import webdriver
import unittest


class UserBrowsingLibraryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    # User enters the all boks page and is able to see all books

    # User tries to search book by author
    # Library returns correct set of books displayed in easy-to-read way

    # User tries to search another book by language
    # Library returns correct set of books displayed in easy-to-read way

    # User then searches by date range
    # Library once again returns books published in given date range displayed
    # in easy-to-read way

    # User is satisfied and closes the all books page


class UserAddingNewBookByHandTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    # User enters the editing page

    # User is encouraged to enter the new book data
    # User enters all the data needed
    # The validation of the data is displayed when the data is wrong
    # User corrects the data
    # Data is validated again and user can proceed
    # After clicking enter button the page displays information that the
    # database is updated

    # User enters the browsing page
    # User searches the newly uploaded book
    # The book is correctly displayed
    # User is happy
    # User leaves the browsing page


class UserEditingExistingBookTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    # TBA
