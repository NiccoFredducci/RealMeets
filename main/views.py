from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "edit_event.html"
    pk_url_kwarg = "event_id"

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)

    success_url = reverse_lazy("home")

def home(request):

    role = None
    query = request.GET.get("q", "")

    events = Event.objects.all()
    attendances = Event.objects.none()
    subscribed_ids = set()

    if request.user.is_authenticated:
        role = request.user.profile.role

        if role == "manager":
            events = events.filter(creator=request.user)

        elif role == "subscriber":
            attendances = request.user.subscribed_events.all()

            subscribed_ids = set(
                request.user.subscribed_events.values_list("id", flat=True)
            )
            
            subscribed_ids = set(map(int, subscribed_ids))

            events = events.exclude(subscribers=request.user)
            
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, "home.html", {
        "role": role,
        "events": events,
        "attendances": attendances,
        "query": query,
        "subscribed_ids": subscribed_ids,
    })

@login_required
def create_event(request):

    if request.user.profile.role != "manager":
        return redirect("home")

    event = Event.objects.create(
        title="New Event",
        description="Description",
        creator=request.user,
        background_color="#F7F9F9"
    )

    return redirect("edit_event", event_id=event.id)

@login_required
def delete_event(request, event_id):

    if request.method == "POST":

        event = get_object_or_404(Event, id=event_id)

        if request.user.profile.role != "manager":
            return redirect("home")

        if event.creator != request.user:
            return redirect("home")

        event.delete()

    return redirect("home")

@login_required
def toggle_attendance(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    user = request.user

    if user in event.subscribers.all():
        event.subscribers.remove(user)
        status = "removed"
    else:
        event.subscribers.add(user)
        status = "added"

    return JsonResponse({
        "status": status,
        "event_id": event.id
    })

@login_required
def remove_participant(request, event_id, user_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    event = get_object_or_404(Event, id=event_id)

    if request.user.profile.role != "manager" or event.creator != request.user:
        return JsonResponse({"error": "not allowed"}, status=403)

    user = get_object_or_404(User, id=user_id)

    event.subscribers.remove(user)

    return JsonResponse({
        "status": "removed",
        "user_id": user_id
    })