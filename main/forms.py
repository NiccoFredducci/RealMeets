from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "image", "background_color"]
        
        widgets = {
            "background_color": forms.TextInput(attrs={
                "type": "color"
            }),
        }