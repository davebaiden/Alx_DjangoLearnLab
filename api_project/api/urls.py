from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create the router and register the ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# Define URL patterns
urlpatterns = [
    # ListAPIView for simple listing
    path('books/', BookList.as_view(), name='book-list'),

    # Include all routes from the router (CRUD operations)
    path('', include(router.urls)),
]
