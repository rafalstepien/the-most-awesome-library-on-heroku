from django.shortcuts import render, HttpResponseRedirect
from forms import forms


def submit_new_book(request):
    if request.method == 'POST':

        form = forms.AddBookForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/library')

        else:
            print(form.errors)

    else:
        form = forms.AddBookForm()

    return render(request, 'forms/add_book.html', {'form': form})
