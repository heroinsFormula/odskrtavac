import unicodedata
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books.models import Book, Author
from books.serializer import BookSerializer, AuthorSerializer
from books.helper_functions import evaluate_book_criteria
from django.http import JsonResponse
from django.db.models import Q


def remove_accents(input_str):
    """
    Slouží k normalizaci vstupů.
    Searchbar nebude rozeznávat rozdíl mezi 'Čapek' a 'capek'.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str).lower()
    return ''.join(
        [char for char in nfkd_form if not unicodedata.combining(char)]
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_books(request):
    books = Book.objects.all()

    name = request.query_params.get('name', None)
    poetry = request.query_params.get('poetry', None)
    prose = request.query_params.get('prose', None)
    drama = request.query_params.get('drama', None)
    country = request.query_params.get('country', None)
    century = request.query_params.get('century', None)

    if name:
        normalized_name = remove_accents(name)

        books = [
            book for book in books
            if normalized_name in remove_accents(book.name) or
            normalized_name in remove_accents(book.author.full_name)
            ]

    literary_type_filters = Q()

    if poetry == 'true':
        literary_type_filters |= Q(literary_type='Poezie')
    if prose == 'true':
        literary_type_filters |= Q(literary_type='Próza')
    if drama == 'true':
        literary_type_filters |= Q(literary_type='Drama')

    if literary_type_filters:
        books = books.filter(literary_type_filters)

    if country == "czech":
        books = books.filter(author__country__iexact='CZ')
    elif country == "world":
        books = books.exclude(author__country__iexact='CZ')

    if century == '18th and prior':
        books = books.filter(publish_year__lt=1800)
    elif century == '19th-20th':
        books = books.filter(publish_year__gte=1801, publish_year__lte=1901)
    elif century == '20th-21st':
        books = books.filter(publish_year__gt=1901)

    serializer = BookSerializer(books, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_author(request):
    serializer = AuthorSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_book(request):
    author_full_name = request.data.get('author_full_name')

    if not author_full_name:
        return Response(
            {"message": "Kniha musí mít autora!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    author, created = Author.objects.get_or_create(
        full_name=author_full_name,
        defaults={
            'country': request.data.get('country'),
        }
    )

    book_data = {
        'name': request.data.get('name'),
        'publish_year': request.data.get('publish_year'),
        'literary_type': request.data.get('literary_type'),
        'author': author.id,
    }

    serializer = BookSerializer(data=book_data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_criteria(request):
    criteria = evaluate_book_criteria(request.user)
    return JsonResponse(criteria, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_read_status(request, slug):
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Kniha nebyla nalezena'}, status=404)

    if request.user in book.read_by.all():
        book.read_by.remove(request.user)
        read_status = False
    elif request.user not in book.read_by.all():
        book.read_by.add(request.user)
        read_status = True

    return JsonResponse({'slug': slug, 'is_read': read_status}, status=200)
