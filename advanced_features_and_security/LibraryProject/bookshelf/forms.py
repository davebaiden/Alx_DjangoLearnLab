from django import forms
from .models import Book
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "added_by"]

    publication_year = forms.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(timezone.now().year + 1)]
    )
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)


class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)


class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100, required=True)
