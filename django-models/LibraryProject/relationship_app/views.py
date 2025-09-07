from django.shortcuts import render
from .models import Book
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Library

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()
    # If you want plain text response:
    # book_list = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    # return HttpResponse(book_list, content_type="text/plain")
    
    # If using template:
    return render(request, "list_books.html", {"books": books})

# Class-Based View for Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"  # The variable available in template
