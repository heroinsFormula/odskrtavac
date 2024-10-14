from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

from django_countries.fields import CountryField

class Author(models.Model):    
    full_name = models.CharField(max_length=255, blank=True, null=True)
    alt_name = models.CharField(max_length=255, blank=True, null=True)
    country = CountryField()
    description = models.TextField(default="", blank=True, null=True)
    slug = models.SlugField(default="", blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    read_by = models.ManyToManyField(User, related_name="read_books")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    publish_year = models.SmallIntegerField(blank=True, null=True)
    literary_type = models.CharField(max_length=255)
    literary_genre = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(default="", null=False, allow_unicode=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}")
        super().save(*args, **kwargs)
    

