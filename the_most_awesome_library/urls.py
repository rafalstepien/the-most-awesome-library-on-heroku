from django.urls import path
from . import views
from forms import views as forms_views


urlpatterns = [
    path('', views.index, name='index'),
    path('all_books/', forms_views.browse_books, name='all_books'),
    path('edit/', forms_views.submit_new_book, name='edit'),
]