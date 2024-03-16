from django import forms
from main.models import ContactUsMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUsMessage
        fields = (
            "name",
            "email",
            "message",
        )
