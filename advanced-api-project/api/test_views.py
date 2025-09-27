from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create sample books
        self.book1 = Book.objects.create(title="Book A", author="Author X", publication_year=2001)
        self.book2 = Book.objects.create(title="Book B", author="Author Y", publication_year=2002)

        # Define URLs
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book1.id])

        # ✅ Login the client (this ensures tests run against the test DB)
        self.client.login(username="testuser", password="password123")
    # -------------------------------
    # CRUD Tests
    # -------------------------------

    def test_list_books(self):
        """Test retrieving list of books (public access allowed)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Test retrieving a single book (public access allowed)."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_requires_auth(self):
        """Test creating a new book requires authentication."""
        data = {"title": "Book C", "author": "Author Z", "publication_year": 2003}

        # Without authentication → should fail
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With authentication → should succeed
        response = self.client.post(self.create_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_requires_auth(self):
        """Test updating a book requires authentication."""
        data = {"title": "Updated Book A", "author": "Author X", "publication_year": 2010}

        # Without authentication → should fail
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With authentication → should succeed
        response = self.client.put(self.update_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book A")

    def test_delete_book_requires_auth(self):
        """Test deleting a book requires authentication."""
        # Without authentication → should fail
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With authentication → should succeed
        response = self.client.delete(self.delete_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -------------------------------
    # Filtering, Searching, Ordering
    # -------------------------------

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        response = self.client.get(self.list_url, {"author": "Author X"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Author X")

    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(self.list_url, {"search": "Book A"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book A")

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year."""
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
