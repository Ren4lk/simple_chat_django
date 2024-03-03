from email import message
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from main.forms import ContactForm
from main.models import ContactUsMessage


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

            contact_message = ContactUsMessage(**form.cleaned_data)

            if not request.session.session_key:
                request.session.create()
            contact_message.session_key = request.session.session_key

            contact_message.save()
            return HttpResponseRedirect(reverse("main:contact_us"))

    else:
        form = ContactForm()

    context = {"title": "Contact Us", "form": form}
    return render(request, "main/contact_us.html", context)
