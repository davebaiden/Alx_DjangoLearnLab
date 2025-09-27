from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer
import datetime


# List all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Validate publication_year before creating"""
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.date.today().year
        if publication_year and int(publication_year) > current_year:
            raise ValidationError({"publication_year": "Year cannot be in the future."})
        serializer.save()


# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """Validate publication_year before updating"""
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.date.today().year
        if publication_year and int(publication_year) > current_year:
            raise ValidationError({"publication_year": "Year cannot be in the future."})
        serializer.save()


# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
