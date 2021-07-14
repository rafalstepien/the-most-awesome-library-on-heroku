from django.urls import path
from . import views
from forms import views as edit_page_views


urlpatterns = [
    path('', views.index, name='index'),
    path('all_books/', views.all_books_view, name='all_books'),
    path('edit/', edit_page_views.submit_new_book, name='edit'),
]