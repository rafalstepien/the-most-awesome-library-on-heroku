from django.shortcuts import render


def index_page(request):
    return render(request, 'the_most_awesome_library/home_page.html')
