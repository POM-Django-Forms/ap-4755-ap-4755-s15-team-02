from .models import CustomUser


def get_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return CustomUser.get_by_id(user_id)


def is_librarian(user):
    return user and user.role == 1
