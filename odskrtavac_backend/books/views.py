from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books import helper_functions
from books.models import Book, Author
from books.serializer import CountrySerializer, BookSerializer, AuthorSerializer
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from pprint import pprint
from rest_framework.parsers import JSONParser
from django_countries import countries


class BookListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title_name = request.data.get('title_name')
        author_name = request.data.get('author')
        publish_year = request.data.get('publish_year')
        country = request.data.get('country')
        literary_type = request.data.get('literary_type')

        if not all([title_name, author_name, publish_year, country, literary_type]):
            return Response(
                data={'error': 'All fields are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        author = helper_functions.find_author(author_name)
        if not author:
            return Response(
                data={'error': 'Author could not be found or created.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        book_data = {
            'title_name': title_name,
            'author_id': author.id,
            'publish_year': publish_year,
            'country': country,
            'literary_type': literary_type
        }

        serializer = BookSerializer(data=book_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'message': 'Kniha byla vytvořena!', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, slug):

        try:
            book = Book.objects.get(slug=slug)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        title_name = request.data.get('title_name')
        author_name = request.data.get('author')
        publish_year = request.data.get('publish_year')
        country = request.data.get('country')
        literary_type = request.data.get('literary_type')
        if not all([title_name, author_name, publish_year, country, literary_type]):
            return Response(
                data={'error': 'All fields are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        author: Author = helper_functions.find_author(author_name)
        if not author:
            return Response(
                data={'error': 'Author could not be found or created.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        book_data = {
            'title_name': title_name,
            'author_id': author.id,
            'publish_year': publish_year,
            'country': country,
            'literary_type': literary_type
        }

        serializer = BookSerializer(book, data=book_data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'message': 'Kniha byla upravena!', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, slug):
        try:
            book = Book.objects.get(slug=slug)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        book.delete()
        return Response(
            {'message': 'Book deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
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

    return JsonResponse({'slug': slug, 'isRead': read_status}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_countries(request):
    country_list = [{'name': name} for code, name in countries]
    return Response(country_list, status=status.HTTP_200_OK)