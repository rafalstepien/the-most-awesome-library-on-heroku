from django.shortcuts import render, HttpResponseRedirect
from forms import forms
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

            return HttpResponseRedirect('/library')
        else:
            print(form.errors)

    else:
        form = forms.AddBookForm()

    return render(request, 'forms/add_book.html', {'form': form})
