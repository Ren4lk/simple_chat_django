from django import forms

from main.models import ContactMessage


class ContactForm(forms.Form):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message",)
        
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
