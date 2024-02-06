from django.shortcuts import render


# Create your views here.
def chat(request):
    context = {
        "title": "Chat",
    }
    return render(request, "chat/index.html", context)
