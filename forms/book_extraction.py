from the_most_awesome_library.models import Book
from urllib.request import urlopen
import json



def find_books_from_google_API_by_keywords(keywords):
    search_terms = format_keywords(keywords)
    response = urlopen(f'https://www.googleapis.com/books/v1/volumes?q={search_terms}')
    books = load_response_to_dict(response)
    books = extract_just_neccessary_info(books)
    return books


def format_keywords(keywords):
    return '+'.join(keywords.split(' '))


def load_response_to_dict(response):
    data = json.loads(response.read())
    return data['items']


def extract_just_neccessary_info(books):
    books_with_just_neccessary_info = []

    for book in books:
        book_info_extractor = BookInfoExtractor(book)
        book_info = book_info_extractor.get_book_info()
        books_with_just_neccessary_info.append(book_info)
    
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
            title = None
        
        return title
    
    def get_book_author(self):
        try:
            author = ', '.join(self.book_info_dictionary['volumeInfo']['authors'])
        except KeyError:
            author = None
        
        return author
    
    def get_book_published_date(self):
        try:
            published_date = self.book_info_dictionary['volumeInfo']['publishedDate']
        except KeyError:
            published_date = None
        
        return published_date

    def get_book_isbn_number(self):

        try:
            isbn = [isbn_type['identifier'] for isbn_type in 
                    self.book_info_dictionary['volumeInfo']['industryIdentifiers']
                    ][0]
        except KeyError:
            isbn = None
        
        return isbn
    
    def get_book_page_count(self):
        try:
            page_count = self.book_info_dictionary['volumeInfo']['pageCount']
        except KeyError:
            page_count = None

        return page_count
    
    def get_book_thumbnail(self):
        try:
            thumbnail = self.book_info_dictionary['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            thumbnail = None
        
        return thumbnail
    
    def get_book_language(self):
        try:
            language = self.book_info_dictionary['volumeInfo']['language']
        except KeyError:
            language = None
        
        return language
