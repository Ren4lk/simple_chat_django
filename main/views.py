from django.shortcuts import render, redirect
from django.contrib import messages

from main.forms import ContactForm
from main.models import ContactUsMessage


def about(request):
    context = {
        "title": "About",
        "title_of_text": "About us",
        "text_on_page": "It's a simple chat app created with Django for educational purposes.",
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
            messages.success(request, "Your message has been sent successfully!")
            return redirect("main:contact_us")
    else:
        form = ContactForm()

    context = {"title": "Contact Us", "form": form}
    return render(request, "main/contact_us.html", context)
