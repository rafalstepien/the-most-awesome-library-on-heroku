from django.shortcuts import render, HttpResponseRedirect
from forms import forms
from the_most_awesome_library.models import Book
from forms.book_extraction import find_books_from_google_API_by_keywords
from django.contrib import messages
from forms.utils import delete_button_is_clicked, get_clicked_button_id, BookFilterer
from rest_framework import viewsets
from the_most_awesome_library.serializers import BookSerializer
from the_most_awesome_library.models import Book


def add_new_book_view(request):
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
            messages.success(
                request, '''Book has been succesfully dumped to the
                database! You can now browse it in "Browse books" section''')
            return HttpResponseRedirect('/add_book')

    else:
        form = forms.AddBookForm()

    return render(request, 'forms/add_book.html', {'form': form})


def edit_book_view(request):
    if request.method == 'POST':
        form = forms.EditBookForm(request.POST)
        book_id = request.GET['book_id']

        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            publication_date = form.cleaned_data.get('publication_date')
            isbn_number = form.cleaned_data.get('isbn_number')
            pages_number = form.cleaned_data.get('pages_number')
            cover_link = form.cleaned_data.get('cover_link')
            language = form.cleaned_data.get('language')

            book_to_be_edited = Book.objects.get(pk=book_id)
            book_to_be_edited.title = title
            book_to_be_edited.author = author
            book_to_be_edited.publication_date = publication_date
            book_to_be_edited.isbn_number = isbn_number
            book_to_be_edited.pages_number = pages_number
            book_to_be_edited.cover_link = cover_link
            book_to_be_edited.language = language
            book_to_be_edited.save()

            messages.success(request, 'Book has been updated')
            return HttpResponseRedirect('/all_books')

    else:
        book_id = request.GET['book_id']
        book_to_be_edited = Book.objects.get(pk=book_id)
        form = forms.EditBookForm(initial={
            'title': book_to_be_edited.title,
            'author': book_to_be_edited.author,
            'isbn_number': book_to_be_edited.isbn_number,
            'pages_number': book_to_be_edited.pages_number,
            'cover_link': book_to_be_edited.cover_link,
            'language': book_to_be_edited.language,
            'publication_date': book_to_be_edited.publication_date,
        })

    return render(request, 'forms/edit_book.html', {'form': form})


def browse_books_view(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)

        if delete_button_is_clicked(request.POST):
            button_id = get_clicked_button_id(request.POST)
            book_to_delete = Book.objects.get(pk=button_id)
            book_to_delete.delete()

        if form.is_valid():
            queryset = Book.objects.all()
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            language = form.cleaned_data.get('language')
            date_after = form.cleaned_data.get('date_after')
            date_before = form.cleaned_data.get('date_before')

            book_filterer = BookFilterer(
                queryset, title, author, language, date_after, date_before)
            matching_books = book_filterer.build_queryset().order_by('id')

    else:
        form = forms.SearchForm()
        matching_books = Book.objects.all().order_by('id')

    return render(request, 'forms/browse_books.html',
                  {'form': form, 'all_books': matching_books})


def add_new_book_by_keywords_view(request):
    if request.method == 'POST':
        form = forms.SearchKeywordForm(request.POST)

        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            found_books = find_books_from_google_API_by_keywords(keywords)

            if 'ad-to-database-button' in request.POST:
                for book in found_books:
                    book.save()
                messages.success(
                    request, '''All books from table below have been succesfully dumped to the
                database! You can now browse them in "Browse books" section''')

    else:
        form = forms.SearchKeywordForm()
        found_books = None

    return render(request, 'forms/add_book_by_keywords.html',
                  {'form': form, 'found_books': found_books})



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
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')

        book_filterer = BookFilterer(
            queryset,
            title,
            author,
            language,
            date_after,
            date_before)
        queryset = book_filterer.build_queryset()
        return queryset
