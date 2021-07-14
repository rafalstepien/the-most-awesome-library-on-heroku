from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_books/', views.all_books_view, name='all_books'),
    path('edit/', views.edit_view, name='edit'),
]