from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Author(models.Model):
    full_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    alt_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    description = models.TextField(
        default="", blank=True, null=True
    )
    slug = models.SlugField(
        default="", blank=True
    )

    def __str__(self) -> str:
        return f"{self.full_name}" if self.full_name else "Neznámý autor"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, blank=True, null=True
    )
    country = CountryField()
    read_by = models.ManyToManyField(
        User, related_name="read_books"
    )
    description = models.TextField(
        blank=True, null=True
    )
    publish_year = models.SmallIntegerField(
        blank=True, null=True
    )
    literary_type = models.CharField(
        max_length=255
    )
    literary_genre = models.CharField(
        max_length=255, blank=True, null=True
    )
    slug = models.SlugField(
        default="", null=False, allow_unicode=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}")
        super().save(*args, **kwargs)
