import datetime
from django.db.models import Count
from reviews.models import Review


def average_rating(rating_list):
    if not rating_list:
        return 0

    return round(sum(rating_list) / len(rating_list))


def get_books_read_by_month(username):
    current_year = datetime.datetime.now().year
    books = Review.objects.filter(creator__username__contains=username, date_created__year=current_year).values(
        'date_created__month').annotate(book_count=Count('book__title'))
    return books


def get_books_read_by_user(username):
    books = Review.objects.filter(creator__username__contains=username).all()
    return books
