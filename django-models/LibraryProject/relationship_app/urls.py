from django.urls import path
from django.contrib.auth.views import LoginView 
from django.contrib.auth.views import LogoutView
from .views import list_books
from .views import LibraryDetailView
from .views import register_view
from .views import login_view
from .views import logout_view
from .views import add_book
from .views import edit_book
from .views import delete_book
from .views import admin_view
from .views import librarian_view
from .views import member_view

urlpatterns = [
    # Function-Based View for listing books
    path("books/", list_books, name="list_books"),

    # Class-Based View for library detail
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # User authentication URLs
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Book management URLs (with permissions)
    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:book_id>/", edit_book, name="edit_book"),
    path("delete_book/<int:book_id>/", delete_book, name="delete_book"),

    # Role-based access URLs
    path("admin_view/", admin_view, name="admin_view"),
    path("librarian_view/", librarian_view, name="librarian_view"),
    path("member_view/", member_view, name="member_view"),
]
