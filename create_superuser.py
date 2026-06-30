import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventsite.settings")
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin_demo",
        password="admin12345"
    )