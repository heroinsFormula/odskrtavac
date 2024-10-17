from collections import Counter

def evaluate_book_criteria(user):
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