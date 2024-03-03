from django import forms

from main.models import ContactUsMessage


class ContactForm(forms.Form):
    class Meta:
        model = ContactUsMessage
        fields = ("name", "email", "message",)
        
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
