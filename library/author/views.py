from django.shortcuts import render, redirect
from authentication.utils import get_user, is_librarian
from .models import Author
from .forms import AuthorForm  
from book.models import Book


def authors_list(request):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")
    authors = Author.objects.all()
    return render(request, "authors/list.html", {"authors": authors, "user": user})


def create_author(request):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect("/authors/")
    else:
        form = AuthorForm()  

    return render(request, "authors/create.html", {"user": user, "form": form})


def delete_author(request, id):
    user = get_user(request)
    if not is_librarian(user):
        return redirect("/")
    author = Author.get_by_id(id)
    if author:
        if not Book.objects.filter(authors=author).exists():
            Author.delete_by_id(id)
    return redirect("/authors/")
