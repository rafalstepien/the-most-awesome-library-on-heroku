from django.shortcuts import render, HttpResponseRedirect
from forms import forms
from datetime import date
from the_most_awesome_library.models import Book


def submit_new_book(request):
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
                .filter(title__contains=f'{title}') \
                .filter(author__contains=f'{author}') \
                .filter(language__contains=f'{language}') \
                .filter(publication_date__range=[date_after, date_before])

    else:
        form = forms.SearchForm()
        matching_books = Book.objects.all()
    
    return render(request, 'forms/browse_books.html', {'form': form,
                                                       'all_books': matching_books})