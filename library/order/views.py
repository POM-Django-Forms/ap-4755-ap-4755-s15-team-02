from django.utils import timezone
from django.shortcuts import render, redirect
from authentication.utils import get_user, is_librarian
from .models import Order
from .forms import OrderForm


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
        form = OrderForm(request.POST)
        if form.is_valid():
            # commit=False створює об'єкт замовлення в пам'яті, не записуючи в БД
            order = form.save(commit=False)
            order.user = user  #  прив'язуємо поточного авторизованого юзера
            
            #  перевірка наявності книги 
            book = order.book
            if Order.objects.filter(book=book, end_at__isnull=True).count() < book.count:
                order.save()      # зберігаємо замовлення
                book.count -= 1   # зменшуємо кількість книг у бібліотеці
                book.save()
                return redirect("/my-orders/")
            else:
                form.add_error('book', "На жаль, усі примірники цієї книги зараз зайняті.")
    else:
        initial_data = {}
        selected_book_id = request.GET.get("book_id")
        if selected_book_id:
            initial_data['book'] = selected_book_id
            
        form = OrderForm(initial=initial_data)

    return render(request, "orders/create.html", {"form": form, "user": user})


def close_order(request, id):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")
    order = Order.get_by_id(id)
    if order:
        order.update(end_at=timezone.now())
    return redirect("/orders/")
