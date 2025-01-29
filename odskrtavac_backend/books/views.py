from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books import helper_functions
from books.models import Book, Author
from books.serializer import BookSerializer, AuthorSerializer
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from pprint import pprint


class BookListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        author_name = request.data.get('author_name')
        author = helper_functions.find_author(author_name)
        request.data['author'] = author
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Kniha byla vytvořena!'},
            status=status.HTTP_201_CREATED
        )


class AuthorListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booklist_attributes(request):
    criteria = helper_functions.evaluate_book_criteria(user=request.user)
    return JsonResponse(criteria, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_read_status(request, slug):
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Kniha nebyla nalezena'}, status=404)

    user_has_read_book: bool = request.user in book.read_by.all()
    if user_has_read_book:
        book.read_by.remove(request.user)
        read_status = False

    elif not user_has_read_book:
        book.read_by.add(request.user)
        read_status = True

    return JsonResponse({'slug': slug, 'isRead': read_status}, status=200) # status=status.HTTP_200 lepší?
