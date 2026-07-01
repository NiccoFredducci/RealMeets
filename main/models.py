from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    ROLE_CHOICES = [
        ("subscriber", "Subscriber"),
        ("manager", "Manager"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to="event_images/",
        blank=True,
        null=True
    )
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
    
        return "https://i.imgur.com/dXaSfL3.png"

    background_color = models.CharField(
        max_length=7,
        default="#F7F9F9"
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events"
    )

    subscribers = models.ManyToManyField(
        User,
        related_name="subscribed_events",
        blank=True
    )

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role="subscriber")