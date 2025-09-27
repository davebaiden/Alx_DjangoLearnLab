from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer
import datetime


# List all books OR create a new book
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 👈 added

    def perform_create(self, serializer):
        """Extra validation when creating a book"""
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.date.today().year

        if publication_year and int(publication_year) > current_year:
            raise ValidationError({"publication_year": "Year cannot be in the future."})

        serializer.save()


# Retrieve, update, or delete a single book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 👈 added

    def perform_update(self, serializer):
        """Extra validation when updating a book"""
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.date.today().year

        if publication_year and int(publication_year) > current_year:
            raise ValidationError({"publication_year": "Year cannot be in the future."})

        serializer.save()
