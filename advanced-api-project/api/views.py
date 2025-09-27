from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer
import datetime


# List all books (open to everyone)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # 👈 explicit


# Retrieve a single book by ID (open to everyone)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # 👈 explicit


# Create a new book (only authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # 👈 explicit

    def perform_create(self, serializer):
        """Validate publication_year before creating"""
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.date.today().year
        if publication_year and int(publication_year) > current_year:
            raise ValidationError({"publication_year": "Year cannot be in the future."})
        serializer.save()


# Update an existing book (only authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # 👈 explicit

    def perform_update(self, serializer):
        """Validate publication_year before updating"""
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.date.today().year
        if publication_year and int(publication_year) > current_year:
            raise ValidationError({"publication_year": "Year cannot be in the future."})
        serializer.save()


# Delete a book (only authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # 👈 explicit
