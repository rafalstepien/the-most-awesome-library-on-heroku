from django import forms
from django.forms import ModelForm
from the_most_awesome_library.models import Book
from bootstrap_datepicker_plus import DatePickerInput


class DateInput(forms.DateInput):
    input_type = 'date'


class AddBookForm(ModelForm):
    title = forms.CharField(label='Book title', max_length=100, required=True)
    author = forms.CharField(
        label='Author name', max_length=100, required=True)
    isbn_number = forms.CharField(
        label='ISBN number', max_length=100, required=True)
    pages_number = forms.IntegerField(label='Number of pages', required=True)
    cover_link = forms.CharField(
        label='Link to cover', max_length=100, required=True)
    language = forms.CharField(
        label='Publication language', max_length=100, required=True)

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
        widgets = {
            'publication_date': DateInput(),
        }
