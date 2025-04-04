from rest_framework import serializers
from .models import Author, Book
from django_countries.serializer_fields import CountryField
from django_countries.fields import Country

class CountrySerializer(serializers.Serializer):
    country = CountryField()

class TranslatedCountryField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Country):
            return value.name
        return value

    def to_internal_value(self, data):
        return Country(data)

class AuthorSerializer(serializers.ModelSerializer):
    country = TranslatedCountryField()

    class Meta:
        model = Author
        fields = [
            'full_name',
            'alt_name',
            'country'
        ]

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True)
    country = TranslatedCountryField()
    is_read_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title_name',
            'author',
            'author_id',
            'country',
            'publish_year',
            'literary_type',
            'is_read_by_user',
            'slug'
        ]

        read_only_fields = [
            'id',
            'slug',
            'is_read_by_user'
        ]

    def get_is_read_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            isRead = obj.read_by.filter(
                id=request.user.id
            ).exists()
            return isRead
        return False

    def create(self, validated_data):
        author = validated_data.pop('author_id')
        country = validated_data.pop('country')
        book = Book.objects.create(author=author, country=country, **validated_data)
        return book

    def update(self, instance, validated_data):
        # Handle author update if provided
        if 'author_id' in validated_data:
            instance.author = validated_data.pop('author_id')

        # Handle country update if provided
        if 'country' in validated_data:
            instance.country = validated_data.pop('country')

        # Update all other fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance