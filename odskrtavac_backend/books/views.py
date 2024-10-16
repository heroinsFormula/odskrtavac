from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books.models import Book
from books.serializer import BookSerializer
from django.http import JsonResponse
from collections import Counter


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True, context={'request': request})
    return Response(serializer.data)

def evaluate_book_requirements(user):
    books = user.read_books.all()
    criteria = {
        "Světová a česká do 18. století": 0,
        "Světová a česká 19. století": 0,
        "Světová 20. a 21. století": 0,
        "Česká 20. a 21. století": 0,
        "Próza":0,
        "Poezie":0,
        "Drama":0,
        "Celkem": 0,
        "Duplicitní autoři":[]
    }
    authors = []
    criteria["Celkem"] = len(books)

    for book in books:
        publish_year = book.publish_year
        country = book.author.country
        literary_type = book.literary_type

        authors.append(book.author)

        match publish_year, country:
            case year, _ if year <= 1800:
                criteria["Světová a česká do 18. století"] += 1
            case year, _ if 1801 <= year <= 1900:
                criteria["Světová a česká 19. století"] += 1
            case _, country if country != "CZ":
                criteria["Světová 20. a 21. století"] += 1
            case _, "CZ":
                criteria["Česká 20. a 21. století"] += 1

        match literary_type:
            case "Próza":
                criteria["Próza"] += 1
            case "Poezie":
                criteria["Poezie"] += 1
            case "Drama":
                criteria["Drama"] += 1

    count_authors = Counter(authors)
    for author, occurrences in count_authors.items():
        if occurrences > 2:
            criteria["Duplicitní autoři"].append(author.full_name)

    return criteria



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
    
    criteria = evaluate_book_requirements(request.user)

    return JsonResponse({'slug': slug, 'read': read_status, 'criteria': criteria})
