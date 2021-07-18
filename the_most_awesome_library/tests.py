from datetime import date
import unittest
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from the_most_awesome_library.views import index_page
from forms.views import (browse_books_view,
                         add_new_book_view)
from forms.book_extraction import (BookInfoExtractor,
                                   SmartDatetimeParser,
                                   extract_just_neccessary_info,
                                   format_keywords,
                                   load_response_to_dict)


class HomePageTest(TestCase):

    def test_root_resolves_to_home_page_view(self):
        resolved_function = resolve('/')
        self.assertEqual(
            resolved_function.func,
            index_page)

    def test_home_page_view_contains_correct_html(self):
        request = HttpRequest()
        response = index_page(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>Awesome Library</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>\n'))


class BrowseBooksPageTest(TestCase):

    def test_books_resolves_to_all_books_view(self):
        resolved_function = resolve('/all_books/')
        self.assertEqual(resolved_function.func,
                         browse_books_view)

    def test_books_view_contains_correct_html(self):
        request = HttpRequest()
        response = index_page(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>Awesome Library</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>\n'))


class AddBookPageTest(TestCase):

    def test_add_book_resolves_to_add_books_view(self):
        resolved_function = resolve('/add_book/')
        self.assertEqual(resolved_function.func, add_new_book_view)

    def test_add_book_view_contains_correct_html(self):
        request = HttpRequest()
        response = index_page(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>Awesome Library</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>\n'))


class BookExtractionTest(unittest.TestCase):

    def test_format_keywords(self):
        keywords1 = 'inauthor:keyes ubik'
        keywords2 = ''
        keywords3 = ' '
        keywords4 = ' test '

        formatted_keywords1 = format_keywords(keywords1)
        formatted_keywords2 = format_keywords(keywords2)
        formatted_keywords3 = format_keywords(keywords3)
        formatted_keywords4 = format_keywords(keywords4)

        self.assertEqual(formatted_keywords1, 'inauthor:keyes+ubik')
        self.assertEqual(formatted_keywords2, '')
        self.assertEqual(formatted_keywords3, '')
        self.assertEqual(formatted_keywords4, 'test')

    def test_load_response_to_dict(self):
        test_response1 = '{"items":{"name":"John"}}'
        test_response2 = '{}'

        parsed_response1 = load_response_to_dict(test_response1)
        parsed_response2 = load_response_to_dict(test_response2)

        self.assertEqual(parsed_response1, {"name": "John"})
        self.assertEqual(parsed_response2, {})

    def test_extract_just_neccessary_info(self):
        test_book = 'the_most_awesome_library/test_data/example_book.json'
        with open(test_book, 'r') as file:
            test_book = file.read()

        data = load_response_to_dict(test_book)
        parsed_data = extract_just_neccessary_info(data)[0]

        self.assertTrue(hasattr(parsed_data, 'title'))
        self.assertTrue(hasattr(parsed_data, 'author'))
        self.assertTrue(hasattr(parsed_data, 'publication_date'))
        self.assertTrue(hasattr(parsed_data, 'isbn_number'))
        self.assertTrue(hasattr(parsed_data, 'pages_number'))
        self.assertTrue(hasattr(parsed_data, 'cover_link'))
        self.assertTrue(hasattr(parsed_data, 'language'))


class BookInfoExtractorTest(unittest.TestCase):
    empty_extractor = BookInfoExtractor({})

    def test_get_book_title(self):
        self.assertEqual(self.empty_extractor.get_book_title(), '')

    def test_get_book_author(self):
        self.assertEqual(self.empty_extractor.get_book_author(), '')

    def test_get_book_published_date(self):
        self.assertEqual(
            self.empty_extractor.get_book_published_date(),
            date(
                1,
                1,
                1))

    def test_get_book_isbn_number(self):
        self.assertEqual(self.empty_extractor.get_book_isbn_number(), '')

    def test_get_book_pages_number(self):
        self.assertEqual(self.empty_extractor.get_book_page_count(), 0)

    def test_get_book_cover(self):
        self.assertEqual(self.empty_extractor.get_book_thumbnail(), '')

    def test_get_book_language(self):
        self.assertEqual(self.empty_extractor.get_book_language(), '')


class SmartDateTimeParserTest(unittest.TestCase):
    def test_full_date_is_passed(self):
        full_date = SmartDatetimeParser('2002-05-10').parse()
        self.assertEqual(full_date, date(2002, 5, 10))

    def test_just_year_and_month_is_passed(self):
        just_year_and_month = SmartDatetimeParser('2002-05').parse()
        self.assertEqual(just_year_and_month, date(2002, 5, 1))

    def test_just_year_is_passed(self):
        just_year = SmartDatetimeParser('2002').parse()
        self.assertEqual(just_year, date(2002, 1, 1))

    def test_empty_date_is_passed(self):
        empty_parser = SmartDatetimeParser('').parse()
        self.assertEqual(empty_parser, date(1, 1, 1))
