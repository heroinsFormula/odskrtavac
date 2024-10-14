from typing import Any
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import generic
from books.models import Author, Book
from books.serializer import AuthorSerializer, BookSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

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


class IndexView(generic.ListView):
    template_name = "books/index.html"
    context_object_name = "books_list"

    def get_queryset(self):
        return Book.objects.order_by("name")
    
    
class AuthorDetailView(generic.DetailView):
    template_name = "books/author_detail.html"
    model = Author

class BookDetailView(generic.DetailView):
    template_name = "books/book_detail.html"
    model = Book
