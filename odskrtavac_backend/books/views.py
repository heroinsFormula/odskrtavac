from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from books.models import Book
from books.serializer import BookSerializer
from django.http import JsonResponse
from .helper_functions import evaluate_book_criteria

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    books = Book.objects.all()
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
