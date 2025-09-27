from rest_framework import serializers
from .models import Author, Book
import datetime


# BookSerializer is responsible for converting Book model instances into JSON (and vice versa).
# It also includes validation to prevent invalid data entry.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation to ensure publication year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# AuthorSerializer is responsible for serializing Author instances.
# It includes a nested representation of related books using BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
