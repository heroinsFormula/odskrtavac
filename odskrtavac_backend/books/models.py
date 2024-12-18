from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Author(models.Model):
    fullName: str = models.CharField(max_length=255)
    slug: str = models.SlugField(default="", max_length=255)
    country: str = CountryField()
    altName: str = models.CharField(default="", max_length=255, blank=True, null=True)
    description: str = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.fullName}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fullName)
        super().save(*args, **kwargs)


class Book(models.Model):
    titleName: str = models.CharField(max_length=255)
    slug: str = models.SlugField(default="")
    country: str = CountryField()
    publishYear: int = models.SmallIntegerField()
    literaryType: str = models.CharField(max_length=255)
    literaryGenre: str = models.CharField(max_length=255, blank=True, null=True)
    description: str = models.TextField(blank=True, null=True)
    author: int = models.ForeignKey(
        Author, on_delete=models.SET_NULL, blank=True, null=True
    )
    readBy: int = models.ManyToManyField(
        User, related_name="readBooks", blank=True
    )

    def __str__(self):
        return f"{self.titleName}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.titleName}")
        if self.author is not None:
            self.country = self.author.country
        super().save(*args, **kwargs)
