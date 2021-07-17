from the_most_awesome_library.serializers import BookSerializer
from django.shortcuts import render, HttpResponseRedirect
from forms import forms
from datetime import date
from the_most_awesome_library.models import Book
from forms.book_extraction import *
from django.contrib import messages
from rest_framework import viewsets


def add_new_book(request):
    if request.method == 'POST':

        form = forms.AddBookForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            publication_date = form.cleaned_data.get('publication_date')
            isbn_number = form.cleaned_data.get('isbn_number')
            pages_number = form.cleaned_data.get('pages_number')
            cover_link = form.cleaned_data.get('cover_link')
            language = form.cleaned_data.get('language')

            book = Book(
                title=title,
                author=author,
                publication_date=publication_date,
                isbn_number=isbn_number,
                pages_number=pages_number,
                cover_link=cover_link,
                language=language,
            )

            book.save()
            messages.success(request, '''Book has been succesfully dumped to the 
                database! You can now browse it in "Browse books" section''')
            return HttpResponseRedirect('/add_book')

    else:
        form = forms.AddBookForm()

    return render(request, 'forms/add_book.html', {'form': form})


def browse_books(request):
    if request.method == 'POST':

        form = forms.SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            language = form.cleaned_data.get('language')
            date_after = form.cleaned_data.get('date_after')
            date_before = form.cleaned_data.get('date_before')

            date_after = date(1, 1, 1) if date_after is None else date_after
            date_before = date.today() if date_before is None else date_before

            matching_books = Book.objects.all() \
                .filter(title__icontains=f'{title}') \
                .filter(author__icontains=f'{author}') \
                .filter(language__icontains=f'{language}') \
                .filter(publication_date__range=[date_after, date_before])

    else:
        form = forms.SearchForm()
        matching_books = Book.objects.all()

    return render(request, 'forms/browse_books.html', {'form': form,
                                                       'all_books': matching_books})


def add_new_book_by_keywords(request):
    if request.method == 'POST':
        form = forms.SearchKeywordForm(request.POST)

        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            found_books = find_books_from_google_API_by_keywords(keywords)

            if 'ad-to-database-button' in request.POST:
                for book in found_books:
                    book.save()
                messages.success(request, '''All books from table below have been succesfully dumped to the 
                database! You can now browse them in "Browse books" section''')

    else:
        form = forms.SearchKeywordForm()
        found_books = None

    return render(request, 'forms/add_book_by_keywords.html', {'form': form,
                                                               'found_books': found_books})


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        language = self.request.query_params.get('language')
        publication_date = self.request.query_params.get('publication_date')

        if title is not None:
            queryset = queryset.filter(title__icontains=f'{title}')
        
        if author is not None:
            queryset = queryset.filter(author__icontains=f'{author}')

        if language is not None:
            queryset = queryset.filter(language__icontains=f'{language}')

        if publication_date is not None:
            queryset = queryset.filter(publication_date__icontains=f'{publication_date}')
        
        return queryset
