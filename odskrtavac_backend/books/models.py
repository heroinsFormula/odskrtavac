from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(default="", max_length=255)
    country = CountryField()
    alt_name = models.CharField(default="", max_length=255, blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Book(models.Model):
    title_name = models.CharField(max_length=255)
    slug = models.SlugField(default="")
    country = CountryField()
    publish_year = models.SmallIntegerField()
    literary_type = models.CharField(max_length=255)
    literary_genre = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        to=Author, on_delete=models.SET_NULL, blank=True, null=True
    )
    read_by = models.ManyToManyField(
        to=User, related_name="read_books", blank=True
    )

    def __str__(self):
        return f"{self.title_name}"

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(f"{self.title_name}")
        if self.author is not None:
            self.country = self.author.country
        super().save(*args, **kwargs)
