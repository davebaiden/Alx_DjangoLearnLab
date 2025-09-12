from django.urls import path
from django.contrib.auth.views import LoginView 
from django.contrib.auth.views import LogoutView
from . import views   # ✅ only this import now

urlpatterns = [
    # Function-Based View for listing books
    path("books/", views.list_books, name="list_books"),  # ✅ now "views.list_books"

    # Class-Based View for library detail
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # User authentication URLs
    path("register/", views.register_view, name="register"),  # ✅ now "views.register_view"
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Book management URLs (with permissions)
    path("add_book/", views.add_book, name="add_book"),        # ✅ changed
    path("edit_book/<int:book_id>/", views.edit_book, name="edit_book"),  # ✅ changed
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"),  # ✅ changed

    # Role-based access URLs
    path("admin_view/", views.admin_view, name="admin_view"),          # ✅ changed
    path("librarian_view/", views.librarian_view, name="librarian_view"),  # ✅ changed
    path("member_view/", views.member_view, name="member_view"),      # ✅ changed
]
