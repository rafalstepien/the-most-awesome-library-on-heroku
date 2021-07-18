from django.shortcuts import render
from the_most_awesome_library.models import Book


def index_page(request):
    return render(request, 'the_most_awesome_library/home_page.html')
