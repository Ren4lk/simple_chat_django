from django.shortcuts import render

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
    context = {
        "title": "Contacts",
    }
    return render(request, "main/contact-us.html", context)
