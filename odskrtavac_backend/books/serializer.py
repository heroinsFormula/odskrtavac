from rest_framework import serializers
from .models import Author, Book
from django_countries.serializer_fields import CountryField
from django_countries.fields import Country


class TranslatedCountryField(serializers.Field):
    """Custom serializer field for translating country names."""

    def to_representation(self, value):
        if isinstance(value, Country):
            # Return the translated name of the country
            return value.name
        return value

    def to_internal_value(self, data):
        # Convert the country name or code back into a `Country` instance
        return Country(data)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'full_name',
            'alt_name',
            'country'
        ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    country = TranslatedCountryField()
    is_read_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title_name',
            'author',
            'country',
            'publish_year',
            'literary_type',
            'is_read_by_user',
            'slug'
        ]

    def get_is_read_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            isRead = obj.read_by.filter(
                id=request.user.id
            ).exists()
            return isRead
        return False
