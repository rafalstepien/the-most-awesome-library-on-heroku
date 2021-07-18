from the_most_awesome_library.models import Book
from urllib.request import urlopen
import json
from django.http import HttpResponse
from datetime import datetime, date
from typing import List


def find_books_from_google_API_by_keywords(keywords: str) -> List:
    """Pass keywords and obtain list of book objects matching them

    Args:
        keywords (str): Keywords used to query the Google API

    Returns:
        list: List of Book objects found by passed keywords
    """
    search_terms = format_keywords(keywords)
    response = urlopen(
        f'https://www.googleapis.com/books/v1/volumes?q={search_terms}'
        ).read()
    books = load_response_to_dict(response)
    books = extract_just_neccessary_info(books)
    return books


def format_keywords(keywords: str) -> str:
    """Format passed keywords to match Google API queries

    Args:
        keywords (str): Keywords to be formatted

    Returns:
        str: Keywords in correct format
    """
    return '+'.join(keywords.strip().split(' '))


def load_response_to_dict(response: HttpResponse) -> dict:
    """Make dict of response in JSON format

    Args:
        response (HttpResponse): Web page response

    Returns:
        dict: JSON data packed to dictionary
    """
    data = json.loads(response)
    try:
        return data['items']
    except KeyError:  # when no book is found
        return {}


def extract_just_neccessary_info(books: dict) -> List:
    """Pass dictionary with books data and create list of book objects based on this data

    Args:
        books (dict): All books data 

    Returns:
        [Book]: List of Book objects based on passed data
    """
    books_with_just_neccessary_info = []

    for book in books:
        book_info_extractor = BookInfoExtractor(book)
        book = book_info_extractor.get_book_info()
        books_with_just_neccessary_info.append(book)

    return books_with_just_neccessary_info


class BookInfoExtractor:
    """
    Class handling the extraction of information from book info dictionary and making book objects from it
    """

    def __init__(self, book_info_dictionary):
        self.book_info_dictionary = book_info_dictionary

    def get_book_info(self):
        book = Book(
            title=self.get_book_title(),
            author=self.get_book_author(),
            publication_date=self.get_book_published_date(),
            isbn_number=self.get_book_isbn_number(),
            pages_number=self.get_book_page_count(),
            cover_link=self.get_book_thumbnail(),
            language=self.get_book_language()
        )

        return book

    def get_book_title(self):
        try:
            title = self.book_info_dictionary['volumeInfo']['title']
        except KeyError:
            title = ''

        return title

    def get_book_author(self):
        try:
            author = ', '.join(
                self.book_info_dictionary['volumeInfo']['authors'])
        except KeyError:
            author = ''

        return author

    def get_book_published_date(self):
        try:
            published_date = self.book_info_dictionary['volumeInfo']['publishedDate']
        except KeyError:
            published_date = '0001-01-01'

        published_date = SmartDatetimeParser(published_date).parse()
        return published_date

    def get_book_isbn_number(self):

        try:
            isbn = [isbn_type['identifier'] for isbn_type in
                    self.book_info_dictionary['volumeInfo']['industryIdentifiers']
                    ][0]
        except KeyError:
            isbn = ''

        return isbn

    def get_book_page_count(self):
        try:
            page_count = self.book_info_dictionary['volumeInfo']['pageCount']
        except KeyError:
            page_count = 0

        return page_count

    def get_book_thumbnail(self):
        try:
            thumbnail = self.book_info_dictionary['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            thumbnail = ''

        return thumbnail

    def get_book_language(self):
        try:
            language = self.book_info_dictionary['volumeInfo']['language']
        except KeyError:
            language = ''

        return language


class SmartDatetimeParser:
    """
    Class making datetime objects of passed string, handling the exceptions when partial data is passed
    """
    def __init__(self, datetime_string):
        self.datetime_string = datetime_string

    def parse(self):
        if self.full_date_is_passed():
            datetime_object = datetime.strptime(
                self.datetime_string, '%Y-%m-%d').date()

        elif self.just_year_and_month_is_passed():
            datetime_object = datetime.strptime(
                self.datetime_string, '%Y-%m').date()

        elif self.just_year_is_passed():
            try:
                datetime_object = datetime.strptime(
                    self.datetime_string, '%Y').date()
            except ValueError:
                datetime_object = date(1, 1, 1)

        return datetime_object

    def full_date_is_passed(self):
        return len(self.datetime_string.split('-')) == 3

    def just_year_and_month_is_passed(self):
        return len(self.datetime_string.split('-')) == 2

    def just_year_is_passed(self):
        return len(self.datetime_string.split('-')) == 1
