from django import forms
from django.forms import ModelForm
from the_most_awesome_library.models import Book


class DateInput(forms.DateInput):
    input_type = 'date'


class AddBookForm(ModelForm):
    title = forms.CharField(label='Book title', required=True)
    author = forms.CharField(
        label='Author name', required=True)
    isbn_number = forms.CharField(
        label='ISBN number', required=True)
    pages_number = forms.IntegerField(label='Number of pages', required=True)
    cover_link = forms.CharField(
        label='Link to cover', required=True)
    language = forms.CharField(
        label='Publication language', required=True)
    publication_date = forms.DateField(label="Publication date", widget=forms.widgets.DateInput(attrs={'type': 'date'}))

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


class SearchForm(ModelForm):
    title = forms.CharField(label='Book title', required=False)
    author = forms.CharField(label='Author name', required=False)
    language = forms.CharField(label='Publication language', required=False)
    date_after = forms.DateField(label="Published after", widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    date_before = forms.DateField(label="Published before", widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'language'
        ]


class SearchKeywordForm(forms.Form):
    keywords = forms.CharField(label='Searching keywords', required=True)


class EditBookForm(ModelForm):
    title = forms.CharField(label='Book title', required=True)
    author = forms.CharField(
        label='Author name', required=True)
    isbn_number = forms.CharField(
        label='ISBN number', required=True)
    pages_number = forms.IntegerField(label='Number of pages', required=True)
    cover_link = forms.CharField(
        label='Link to cover', required=True)
    language = forms.CharField(
        label='Publication language', required=True)
    publication_date = forms.DateField(label="Publication date", widget=forms.widgets.DateInput(attrs={'type': 'date'}))

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