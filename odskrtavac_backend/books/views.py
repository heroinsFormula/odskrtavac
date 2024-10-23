from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books.models import Book
from books.serializer import BookSerializer
from django.http import JsonResponse
from .helper_functions import evaluate_book_criteria
from django.db.models import Q


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
        books = books.filter(name__icontains=name)

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
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_criteria(request):
    criteria = evaluate_book_criteria(request.user)
    return JsonResponse(criteria)

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
    else:
        book.read_by.add(request.user)
        read_status = True

    return JsonResponse({'slug': slug, 'read': read_status})
