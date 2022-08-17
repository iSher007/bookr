from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# from django.views.decorators.cache import cache_page

from .forms import *
from .models import *
from .utils import average_rating, get_books_read_by_month, get_books_read_by_user
from django.utils import timezone
import plotly.graph_objs as graphs
from plotly.offline import plot
import xlsxwriter
from io import BytesIO


# @cache_page(60)
def index(request):
    viewed_books = [Book.objects.get(id=book_id[0]) for book_id in request.session.get('viewed_books', [])]

    context = {
        "viewed_books": viewed_books,
    }
    return render(request, "reviews/base.html", context)


def book_search(request):
    search_text = request.GET.get('search', "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data['search']
        search_in = form.cleaned_data['search_in'] or 'title'
        if search_in == 'title':
            books = Book.objects.filter(title__icontains=search)
        else:
            contributors = Contributor.objects.filter(first_names__icontains=search) | Contributor.objects.filter(
                last_names__icontains=search)
            for contributor in contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        if request.user.is_authenticated:
            ss = [search, search_in]
            search_history = request.session.get('search_history', [])
            if ss in search_history:
                search_history.pop(search_history.index(ss))
            search_history.insert(0, ss)
            request.session['search_history'] = search_history[:10]
        # fname_contributors = Contributor.objects.filter(first_names__icontains=search)
        # for contributor in fname_contributors:
        #     for book in contributor.book_set.all():
        #         books.add(book)
        #
        # lname_contributors = Contributor.objects.filter(last_names__icontains=search)
        # for contributor in lname_contributors:
        #     for book in contributor.book_set.all():
        #         books.add(book)
    return render(request, "reviews/search_results.html", {'search_text': search_text, 'form': form, 'books': books})


def book_list(request):
    books = Book.objects.all()
    books_with_reviews = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        books_with_reviews.append({"book": book, "book_rating": book_rating, "number_of_reviews": number_of_reviews})

    context = {
        "book_list": books_with_reviews
    }
    return render(request, "reviews/book_list.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session['viewed_books'] = viewed_books
    return render(request, "reviews/book_detail.html", context)


def is_staff_user(user):
    return user.is_staff


# @permission_required('edit_publisher')
@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, "Publisher \"{}\" created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "reviews/instance-form.html",
                  {"form": form, "instance": publisher, "model_type": "Publisher"})


@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)

        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" updated.".format(book))

            updated_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html",
                  {"form": form, "instance": review, "model_type": "Review", "related_instance": book,
                   "related_model_type": "Book"})


@login_required()
def profile(request):
    user = request.user
    permissions = user.get_all_permissions()
    books_read_by_month = get_books_read_by_month(user.username)
    months = [i + 1 for i in range(12)]
    books_read = [0 for _ in range(12)]

    for num_books_read in books_read_by_month:
        list_index = num_books_read['date_created__month'] - 1
        books_read[list_index] = num_books_read['book_count']
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Month", yaxis_title="No. of books read")
    plot_html = plot(figure, output_type='div')
    return render(request, 'profile.html', {'user': user, 'permissions': permissions, 'books_read_plot': plot_html})


@login_required()
def read_books(request):
    user = request.user
    books = get_books_read_by_user(user)
    temple_file = BytesIO()

    workbook = xlsxwriter.Workbook(temple_file)
    worksheet = workbook.add_worksheet()
    data = []
    for book in books:
        data.append([book.book.title, str(book.date_created)])
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])
    workbook.close()
    data_to_download = temple_file.getvalue()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=reading_history.xlsx'
    response.write(data_to_download)
    return response


def react_example(request):
    return render(request, "react_example.html")
