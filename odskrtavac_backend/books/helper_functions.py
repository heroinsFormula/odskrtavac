from django.db.models.query import QuerySet
from collections import Counter
from django.contrib.auth.models import User
from .models import Author, Book
from typing import List, TypedDict
import unicodedata

def find_author(author_name):
    author = Author.objects.get(full_name=author_name)
    return author

def validate_book_data(request):
    title_name = request.data.get('title_name')
    publish_year = request.data.get('publish_year')
    literary_type = request.data.get('literary_type')
    author_full_name = request.data.get('author_full_name')
    country = request.data.get('country')

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
        'publishYear': publish_year,
        'literaryType': literary_type,
        'country': country,
        'author': author.id if author else None,
    }

def remove_accents(input: str) -> str:
    """
    Slouží k normalizaci vstupů.
    Parametry 'Čapek' a 'capek' najdou stejné tituly.
    """
    nfkd_form = unicodedata.normalize('NFKD', input).lower()
    return ''.join(
        [char for char in nfkd_form if not unicodedata.combining(char)]
    )

class Criteria(TypedDict):
    world_and_czech_pre18th_century: int
    world_and_czech_19th_century: int
    world20th_and21st_century: int
    czech20th_and21st_century: int
    prose: int
    poetry: int
    drama: int
    total: int
    recurring_authors: List[str]

def evaluate_book_criteria(user: User):
    books: QuerySet[Book] = Book.objects.filter(read_by=user)
    criteria: Criteria = {
        "world_and_czech_pre18th_century": 0,
        "world_and_czech_19th_century": 0,
        "world20th_and21st_century": 0,
        "czech20th_and21st_century": 0,
        "prose": 0,
        "poetry": 0,
        "drama": 0,
        "total": 0,
        "recurring_authors": []
    }
    authors: List[Author] = []
    criteria["total"] = len(books)

    for book in books:
        publish_year = book.publish_year
        country = book.country
        literary_type = book.literary_type

        if book.author is not None:
            authors.append(book.author)

        match publish_year, country:
            case year, _ if year <= 1800:
                criteria["world_and_czech_pre18th_century"] += 1
            case year, _ if 1801 <= year <= 1900:
                criteria["world_and_czech_19th_century"] += 1
            case _, country if country != "CZ":
                criteria["world20th_and21st_century"] += 1
            case _, "CZ":
                criteria["czech20th_and21st_century"] += 1

        match literary_type:
            case "Próza":
                criteria["prose"] += 1
            case "Poezie":
                criteria["poetry"] += 1
            case "Drama":
                criteria["drama"] += 1

    count_authors = Counter(authors)
    for author, occurrences in count_authors.items():
        if occurrences > 2:
            criteria["recurring_authors"].append(author.full_name)

    return criteria
