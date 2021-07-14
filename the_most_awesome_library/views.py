from django.shortcuts import render
from the_most_awesome_library.models import Book


def index(request):
    return render(request, 'the_most_awesome_library/home_page.html')


def all_books_view(request):
    all_books = Book.objects.all()
    return render(request, 'the_most_awesome_library/all_books_page.html', {'all_books': all_books})


def edit_view(request):
    return render(request, 'the_most_awesome_library/edit_page.html')

