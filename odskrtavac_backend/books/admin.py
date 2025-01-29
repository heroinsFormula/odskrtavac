from django.contrib import admin
from .models import Book, Author


class Author_admin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "slug",
        "country",
        "alt_name",
        "id",
    )


class Book_admin(admin.ModelAdmin):
    list_display = (
        "title_name",
        "slug",
        "country",
        "literary_type",
        "publish_year",
        "author",
        "id",
    )


admin.site.register(Book, Book_admin)
admin.site.register(Author, Author_admin)
