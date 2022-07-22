from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('books/<int:book_pk>/reviews/new/', review_edit, name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', review_edit, name='review_edit'),
    path('book-search/', book_search, name='book_search'),
    path('publishers/<int:pk>/', publisher_edit, name='publisher_edit'),
    path('publishers/new/', publisher_edit, name='publisher_create'),
    path('accounts/profile/', profile, name='profile'),
]
