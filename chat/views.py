from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(
        request,
        "chat/index.html",
        {
            "current_user": {
                "username": request.user.username,
                "gender": request.user.gender,
            }
        },
    )
