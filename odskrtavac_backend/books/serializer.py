from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'fullName',
            'altName',
            'country'
        ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    isReadByUser: bool = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'titleName',
            'author',
            'country',
            'publishYear',
            'literaryType',
            'slug',
            'isReadByUser',
        ]

    def get_isReadByUser(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            isRead = obj.readBy.filter(
                id=request.user.id
            ).exists()
            return isRead
        return False
