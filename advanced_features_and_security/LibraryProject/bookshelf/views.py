from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .models import Book
from .forms import BookForm, BookSearchForm


# ------------------------------
# Custom CSP decorator (per-view)
# ------------------------------
def csp_protect(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            response["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'"
        return response
    return wrapper


# ------------------------------
# Book List View with Permissions
# ------------------------------
@csrf_protect
@csp_protect
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # safe ORM-based filtering (prevents SQL injection)
            books = books.filter(title__icontains=q)
    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})


# ------------------------------
# Create Book View
# ------------------------------
@csrf_protect
@csp_protect
@permission_required("bookshelf.can_create", raise_exception=True)
@require_http_methods(["GET", "POST"])
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            if not book.added_by_id:
                book.added_by = request.user
            book.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


# ------------------------------
# Edit Book View
# ------------------------------
@csrf_protect
@csp_protect
@permission_required("bookshelf.can_edit", raise_exception=True)
@require_http_methods(["GET", "POST"])
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("book_list")
    return render(request, "bookshelf/form_example.html", {"form": form})


# ------------------------------
# Delete Book View
# ------------------------------
@csrf_protect
@csp_protect
@permission_required("bookshelf.can_delete", raise_exception=True)
@require_http_methods(["POST"])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")
