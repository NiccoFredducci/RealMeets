from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("event/<int:event_id>/edit/", views.EventUpdateView.as_view(), name="edit_event"),
    path("event/<int:event_id>/toggle/", views.toggle_attendance, name="toggle_attendance"),
    path("event/create/", views.create_event, name="create_event"),
    path("event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/remove/<int:user_id>/", views.remove_participant, name="remove_participant"),
]