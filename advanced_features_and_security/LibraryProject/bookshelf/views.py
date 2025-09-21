from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

# ------------------------------
# Book List View with Permissions
# ------------------------------
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
