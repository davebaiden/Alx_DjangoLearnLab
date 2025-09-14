from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "publication_year", "isbn")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "isbn")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    filter_horizontal = ("books",)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "library")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role")
    list_filter = ("role",)
    search_fields = ("user__username",)
