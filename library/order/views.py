from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from authentication.utils import get_user, is_librarian
from .models import Order
from book.models import Book


def orders_list(request):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")
    orders = Order.objects.all()
    return render(request, "orders/list.html", {"orders": orders, "user": user})


def my_orders(request):
    user = get_user(request)
    if not user:
        return redirect("/login/")
    orders = Order.objects.select_related("book").filter(user=user)
    return render(request, "orders/my_orders.html", {"orders": orders, "user": user})


def create_order(request):
    user = get_user(request)
    if not user:
        return redirect("/login/")

    if request.method == "POST":
        book_id = request.POST.get("book_id")
        plated_end_at_raw = request.POST.get("plated_end_at")

        if not plated_end_at_raw:
            return render(
                request,
                "orders/create.html",
                {
                    "books": Book.objects.all(),
                    "selected_book": book_id,
                    "error": "Please select planned end date",
                    "user": user,
                },
            )

        book = Book.get_by_id(book_id)
        plated_end_at = parse_datetime(plated_end_at_raw)

        if book and plated_end_at:
            Order.create(user, book, plated_end_at)
            return redirect("/my-orders/")

    books = Book.objects.all()
    selected_book = request.GET.get("book_id")
    return render(
        request,
        "orders/create.html",
        {"books": books, "selected_book": selected_book, "user": user},
    )


def close_order(request, id):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")
    order = Order.get_by_id(id)
    if order:
        order.update(end_at=timezone.now())
    return redirect("/orders/")
