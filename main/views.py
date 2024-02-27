from email import message
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from main.forms import ContactForm
from main.models import ContactMessage

# Create your views here.


def index(request):
    context = {
        "title": "Main",
    }
    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "About",
        "title_of_text": "About us",
        "text_on_page": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Exercitationem, sit!",
    }
    return render(request, "main/about.html", context)


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            contact_message = ContactMessage(**form.cleaned_data)
            contact_message.save()
            # form.save()
            # form = ContactForm()
            return HttpResponseRedirect(reverse("main:contact-us"))

    else:
        form = ContactForm()

    context = {
        "title": "Contacts",
        'form' : form
    }
    return render(request, "main/contact-us.html", context)
