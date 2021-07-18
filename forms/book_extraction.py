from the_most_awesome_library.models import Book
from urllib.request import urlopen
import json
from datetime import datetime, date


def find_books_from_google_API_by_keywords(keywords):
    search_terms = format_keywords(keywords)
    response = urlopen(
        f'https://www.googleapis.com/books/v1/volumes?q={search_terms}'
        ).read()
    books = load_response_to_dict(response)
    books = extract_just_neccessary_info(books)
    return books


def format_keywords(keywords):
    return '+'.join(keywords.strip().split(' '))


def load_response_to_dict(response):
    data = json.loads(response)
    try:
        return data['items']
    except KeyError:  # when no book is found
        return {}


def extract_just_neccessary_info(books):
    books_with_just_neccessary_info = []

    for book in books:
        book_info_extractor = BookInfoExtractor(book)
        book = book_info_extractor.get_book_info()
        books_with_just_neccessary_info.append(book)

    return books_with_just_neccessary_info


class BookInfoExtractor:

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
            datetime_object = datetime.strptime(
                self.datetime_string, '%Y').date()

        else:
            datetime_object = date(1, 1, 1)

        return datetime_object

    def full_date_is_passed(self):
        return len(self.datetime_string.split('-')) == 3

    def just_year_and_month_is_passed(self):
        return len(self.datetime_string.split('-')) == 2

    def just_year_is_passed(self):
        return len(self.datetime_string.split('-')) == 1
