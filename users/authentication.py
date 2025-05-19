from users.models import User


def create_user(backend, user, *args, **kwargs):
    User.objects.get_or_create(username=user.username)