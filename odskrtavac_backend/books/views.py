import unicodedata
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books import helper_functions
from books.models import Book, Author
from books.serializer import BookSerializer, AuthorSerializer
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

    name_field = request.query_params.get('name', None)
    poetry_field = request.query_params.get('poetry', None)
    prose_field = request.query_params.get('prose', None)
    drama_field = request.query_params.get('drama', None)
    country_field = request.query_params.get('country', None)
    century_field = request.query_params.get('century', None)

    if name_field:
        normalized_name = remove_accents(name_field)
        books = [
            book for book in books
            if normalized_name in remove_accents(book.name) or
            (book.author and normalized_name
             in remove_accents(book.author.full_name))
        ]

    literary_type_filters = Q()

    # Aby user mohl vyhledávat několik typů najednou
    if poetry_field == 'true':
        literary_type_filters |= Q(literary_type='Poezie')
    if prose_field == 'true':
        literary_type_filters |= Q(literary_type='Próza')
    if drama_field == 'true':
        literary_type_filters |= Q(literary_type='Drama')

    if literary_type_filters:
        books = books.filter(literary_type_filters)

    if country_field == "czech":
        books = books.filter(author__country__iexact='CZ')
    elif country_field == "world":
        books = books.exclude(author__country__iexact='CZ')

    if century_field == '18th and prior':
        books = books.filter(publish_year__lte=1800)
    elif century_field == '19th-20th':
        books = books.filter(publish_year__gte=1801, publish_year__lte=1900)
    elif century_field == '20th-21st':
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
@permission_classes([AllowAny])
def post_book(request):
    book_name = request.data.get('name')
    publish_year = request.data.get('publish_year')
    literary_type = request.data.get('literary_type')
    author_full_name = request.data.get('author_full_name')
    country = request.data.get('country')
    no_author: bool = request.data.get('no_author')

    if not country:
        return Response(
            {'message': 'Musí být vyplněna země!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if no_author:
        author = None
    elif not author_full_name:
        return Response(
            {'message': 'Autorovi chybí jméno!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        author, _ = Author.objects.get_or_create(
            full_name=author_full_name,
            country=country
        )

    if Book.objects.filter(name=book_name, author=author).exists():
        return Response(
            {'message': 'Kniha s tímto názvem a autorem již existuje!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book_data = {
        'name': book_name,
        'publish_year': publish_year,
        'literary_type': literary_type,
        'country': country,
        'author': author.id if author else None,
    }

    serializer = BookSerializer(data=book_data)

    serializer.is_valid()
    serializer.save()
    return Response(
        {'message': 'Kniha byla vytvořena!',
            'data': serializer.data},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_criteria(request):
    criteria = helper_functions.evaluate_book_criteria(request.user)
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
