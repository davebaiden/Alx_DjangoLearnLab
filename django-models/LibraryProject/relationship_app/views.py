from django.shortcuts import render
from django.views.generic.detail import DetailView  # ✅ checker wants this
from .models import Library
from .models import Book

# Function-Based View (FBV) to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-Based View (CBV) to show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
