from django.test import TestCase


class HomePageTest(TestCase):
    
    def test_root_resolves_to_home_page_view(self):
        pass

    def test_home_page_view_contains_correct_html(self):
        pass


class BooksPageTest(TestCase):

    def test_books_resolves_to_all_books_view(self):
        pass

    def test_books_view_contains_correct_html(self):
        pass


class EditPageTest(TestCase):

    def test_edit_resolves_to_edit_books_view(self):
        pass

    def test_edit_view_contains_correct_html(self):
        pass