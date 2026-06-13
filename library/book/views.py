from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from authentication.utils import get_user, is_librarian
from .models import Book
from order.models import Order
from .forms import BookForm


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
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect("/books/")
    else:
        form = BookForm()  

    return render(request, "books/create.html", {"form": form, "user": user})

def delete_book(request, id):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/books/")
    
    book = get_object_or_404(Book, id=id)
    
    has_orders = Order.objects.filter(book=book).exists()
    
    if not has_orders:
        book.delete()  
    else:
        pass

    return redirect("/books/")

def edit_book(request, id):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/books/") 
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("/books/")
    else:
        form = BookForm(instance=book)
    return render(request, "books/edit.html", {"form": form, "user": user, "book": book})