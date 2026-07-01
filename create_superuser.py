import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventsite.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile  # adjust if needed


def create_user(username, password, role=None, is_superuser=False):
    if User.objects.filter(username=username).exists():
        return

    user = User.objects.create_user(
        username=username,
        password=password
    )

    if is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save()

    profile, created = Profile.objects.get_or_create(user=user)

    if role:
        profile.role = role
        profile.save()

    return user


admin = create_user(
    username="admin_demo",
    password="admin12345",
    role="manager",
    is_superuser=True
)

create_user(
    username="manager_demo",
    password="manager12345",
    role="manager",
    is_superuser=False
)

create_user(
    username="user_demo",
    password="user12345",
    role="subscriber",
    is_superuser=False
)