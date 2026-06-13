from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import CustomUserForm, LoginForm
from .models import CustomUser
from order.models import Order
from .utils import get_user, is_librarian


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)  
            user.is_active = True
            user.save()

            request.session["user_id"] = user.id
            return redirect("/books/")
    else:
        form = CustomUserForm()

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    error_message = None
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Отримуємо вже очищені та безпечні дані з форми
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user = CustomUser.get_by_email(email)

            if user and check_password(password, user.password):
                request.session["user_id"] = user.id
                return redirect("/books/")
            else:
                error_message = "Невірний email або password"
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form, "error_message": error_message})


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
