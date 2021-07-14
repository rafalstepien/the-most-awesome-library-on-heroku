from django.shortcuts import render


def index(request):
    return render(request, 'the_most_awesome_library/home_page.html')


def all_books_view(request):
    return render(request, 'the_most_awesome_library/all_books_page.html')


def edit_view(request):
    return render(request, 'the_most_awesome_library/edit_page.html')

