from the_most_awesome_library.models import Book
from rest_framework import serializers


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'publication_date',
            'isbn_number',
            'pages_number',
            'cover_link',
            'language',
        ]
