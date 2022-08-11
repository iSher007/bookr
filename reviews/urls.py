from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from . import api_views
from .views import *

router = DefaultRouter()
router.register(r'books', api_views.BookViewSet)
router.register(r'reviews', api_views.ReviewViewSet)

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
    path('api/', include((router.urls, 'api'))),
    path('api/login/', api_views.Login.as_view(), name='login'),
    path('accounts/profile/read_books', read_books, name='read_books'),
    # path('api/all_books/', api_views.all_books.as_view(), name='all_books'),
    # path('api/contributor/', api_views.ContributorView.as_view(), name='contributor_api'),
]
