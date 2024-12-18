from django.contrib import admin
from .models import Book, Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "fullName",
        "slug",
        "country",
        "altName",
        "id",
    )


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "titleName",
        "slug",
        "country",
        "literaryType",
        "publishYear",
        "author",
        "id",
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
