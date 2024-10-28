from django.contrib import admin
from .models import Book, Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "slug",
        "country",
        "alt_name",
        "id",
    )


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "country",
        "literary_type",
        "publish_year",
        "author",
        "id",
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
