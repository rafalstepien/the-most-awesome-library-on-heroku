from django.shortcuts import render, HttpResponseRedirect
from forms import forms


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
            print(title, author, publication_date, isbn_number,
                  pages_number, cover_link, language)

            return HttpResponseRedirect('/library')
        else:
            print(form.errors)

    else:
        form = forms.AddBookForm()

    return render(request, 'forms/add_book.html', {'form': form})
