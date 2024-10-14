from django.contrib import admin
from .models import Book, Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "alt_name", "slug", "id")

class BookAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "publish_year", "literary_type", "slug", "id")


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)