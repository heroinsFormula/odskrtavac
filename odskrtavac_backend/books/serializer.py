from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'full_name',
            'country',
        ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    is_read_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'name',
            'author',
            'publish_year',
            'literary_type',
            'slug',
            'is_read_by_user',
        ]

    def get_is_read_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            is_read = obj.read_by.filter(
                id=request.user.id
            ).exists()
            return is_read
        return False
