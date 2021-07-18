from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(null=True, blank=True)
    isbn_number = models.CharField(max_length=100, null=True, blank=True)
    pages_number = models.IntegerField(null=True, blank=True)
    cover_link = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Book({self.title} by {self.author})'

    def __repr__(self):
        return f'Book({self.title} by {self.author})'
