from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser
from order.models import Order
from .utils import get_user, is_librarian


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = int(request.POST.get("role", 0))

        if not CustomUser.get_by_email(email):
            user = CustomUser.create(email=email, password=make_password(password))
            if user:
                user.role = role
                user.is_active = True
                user.save()
                request.session["user_id"] = user.id
                return redirect("/books/")
    return render(request, "auth/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = CustomUser.get_by_email(email)

        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            return redirect("/books/")
    return render(request, "auth/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("/login/")


def users_list(request):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")
    users = CustomUser.objects.all()
    return render(request, "users/list.html", {"users": users, "user": user})


def user_detail(request, id):
    admin = get_user(request)
    if not is_librarian(admin):
        return redirect("/")
    user_obj = CustomUser.get_by_id(id)
    if not user_obj:
        return redirect("/users/")
    orders = Order.objects.filter(user=user_obj)
    return render(
        request,
        "users/detail.html",
        {"user_obj": user_obj, "orders": orders, "user": admin},
    )
