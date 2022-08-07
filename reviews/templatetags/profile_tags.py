from django import template
from reviews.models import *

register = template.Library()


@register.inclusion_tag('reviews/book_list_tag.html')
def book_list(username):
    reviews = Review.objects.filter(creator__username__contains=username)
    book_list = [review.book.title for review in reviews]
    return {'book_list': book_list}
