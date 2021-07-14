from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn_number = models.CharField(max_length=100)
    pages_number = models.IntegerField()
    cover_link = models.CharField(max_length=200)
    language = models.CharField(max_length=50)

    def __str__(self):
        return f'Book({self.title} by {self.author})'
