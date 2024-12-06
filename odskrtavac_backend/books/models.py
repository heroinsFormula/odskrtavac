from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Author(models.Model):
    full_name: str = models.CharField(max_length=255)
    slug: str = models.SlugField(default="", max_length=255)
    country: str = CountryField()
    alt_name: str = models.CharField(max_length=255, blank=True, null=True)
    description: str = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Book(models.Model):
    name: str = models.CharField(max_length=255)
    slug: str = models.SlugField(default="")
    country: str = CountryField()
    publish_year: int = models.SmallIntegerField()
    literary_type: str = models.CharField(max_length=255)
    literary_genre: str = models.CharField(max_length=255,
                                           blank=True, null=True)
    description: str = models.TextField(blank=True, null=True)
    author: int = models.ForeignKey(
        Author, on_delete=models.SET_NULL, blank=True, null=True
    )
    read_by: int = models.ManyToManyField(
        User, related_name="read_books", blank=True
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}")
        if self.author is not None:
            self.country = self.author.country
        super().save(*args, **kwargs)
