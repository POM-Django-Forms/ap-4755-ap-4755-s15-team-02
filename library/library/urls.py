from django.urls import path
from django.shortcuts import render, redirect
from authentication.views import (
    register,
    login_view,
    logout_view,
    users_list,
    user_detail,
)
from book.views import books_list, book_detail, user_books, create_book, delete_book, edit_book
from order.views import orders_list, create_order, close_order, my_orders
from author.views import authors_list, create_author, delete_author
from authentication.utils import get_user


def home(request):
    user = get_user(request)
    if not user:
        return redirect("/login/")
    return render(request, "home.html", {"user": user})


urlpatterns = [
    path("", home, name="home"),
    # AUTH
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # BOOKS
    path("books/", books_list, name="books"),
    path("books/create/", create_book, name="create_book"),
    path("books/<int:id>/", book_detail, name="book_detail"),
    path("books/user/<int:user_id>/", user_books, name="user_books"),
    path('books/<int:id>/delete/', delete_book, name='delete_book'),
    path('books/<int:id>/edit/', edit_book, name='edit_book'),
    # USERS
    path("users/", users_list, name="users"),
    path("users/<int:id>/", user_detail, name="user_detail"),
    # ORDERS
    path("orders/", orders_list, name="orders"),
    path("orders/create/", create_order, name="create_order"),
    path("orders/<int:id>/close/", close_order, name="close_order"),
    path("my-orders/", my_orders, name="my_orders"),
    # AUTHORS
    path("authors/", authors_list, name="authors"),
    path("authors/create/", create_author, name="create_author"),
    path("authors/delete/<int:id>/", delete_author, name="delete_author"),
]
