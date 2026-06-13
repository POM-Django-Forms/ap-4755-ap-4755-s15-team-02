from django.shortcuts import render, redirect
from django.db.models import Q
from authentication.utils import get_user, is_librarian
from .models import Book
from order.models import Order
from author.models import Author


def books_list(request):
    user = get_user(request)
    if not user:
        return redirect("/login/")

    books = Book.objects.all()
    title = request.GET.get("title", "").strip()
    author = request.GET.get("author", "").strip()

    if title:
        books = books.filter(name__icontains=title)
    if author:
        books = books.filter(
            Q(authors__name__icontains=author)
            | Q(authors__surname__icontains=author)
            | Q(authors__patronymic__icontains=author)
        ).distinct()

    return render(
        request,
        "books/list.html",
        {"books": books, "user": user, "title_query": title, "author_query": author},
    )


def book_detail(request, id):
    user = get_user(request)
    if not user:
        return redirect("/login/")
    book = Book.get_by_id(id)
    if not book:
        return redirect("/books/")
    return render(request, "books/detail.html", {"book": book, "user": user})


def user_books(request, user_id):
    admin = get_user(request)
    if not is_librarian(admin):
        return redirect("/")
    orders = Order.objects.filter(user_id=user_id)
    return render(
        request,
        "books/user_books.html",
        {"orders": orders, "user": admin, "target_user_id": user_id},
    )


def create_book(request):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/books/")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        try:
            count = int(request.POST.get("count") or 1)
        except ValueError:
            count = 1

        author_ids = request.POST.getlist("authors")
        book = Book.objects.create(name=name, description=description, count=count)
        if author_ids:
            authors_qs = Author.objects.filter(id__in=author_ids)
            book.authors.set(authors_qs)
        return redirect("/books/")

    authors = Author.objects.all()
    return render(request, "books/create.html", {"authors": authors, "user": user})
