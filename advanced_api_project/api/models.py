from django.db import models

# The Author model represents a writer.
# Each Author can have multiple books (one-to-many relationship).
class Author(models.Model):
    name = models.CharField(max_length=100)  # Stores the author's name

    def __str__(self):
        return self.name


# The Book model represents a single book.
# Each Book is linked to one Author through a ForeignKey.
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book
    publication_year = models.IntegerField()  # Year the book was published
    author = models.ForeignKey(
        Author,
        related_name="books",   # Allows reverse lookup: author.books.all()
        on_delete=models.CASCADE  # Delete books if the related author is deleted
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
