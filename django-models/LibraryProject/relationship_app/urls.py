from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Function-Based View for listing books
    path('books/', views.list_books, name='list_books'),

    # Class-Based View for library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # User authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),

    # Role-based access URLs
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
