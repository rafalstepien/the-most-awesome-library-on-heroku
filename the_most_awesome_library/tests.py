from django.test import TestCase
from django.urls import resolve
import the_most_awesome_library 
import forms


class HomePageTest(TestCase):
    
    def test_root_resolves_to_home_page_view(self):
        resolved_function = resolve('/')
        self.assertEqual(resolved_function.func, the_most_awesome_library.views.index)

    def test_home_page_view_contains_correct_html(self):
        pass


class BooksPageTest(TestCase):

    def test_books_resolves_to_all_books_view(self):
        resolved_function = resolve('/all_books/')
        self.assertEqual(resolved_function.func, the_most_awesome_library.views.all_books_view)

    def test_books_view_contains_correct_html(self):
        pass


class EditPageTest(TestCase):

    def test_edit_resolves_to_edit_books_view(self):
        resolved_function = resolve('/edit/')
        self.assertEqual(resolved_function.func, forms.views.submit_new_book)

    def test_edit_view_contains_correct_html(self):
        pass