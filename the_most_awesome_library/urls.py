from django.urls import path
from . import views
from forms import views as forms_views


urlpatterns = [
    path('', views.index, name='index'),
    path('all_books/', forms_views.browse_books, name='all_books'),
    path('add_book/', forms_views.add_new_book, name='add_book'),
    path('add_book_by_keywords/', forms_views.add_new_book_by_keywords, name='add_book_by_keywords'),
    path('edit_book/', forms_views.edit_book, name='edit_book')
]
