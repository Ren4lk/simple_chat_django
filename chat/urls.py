from django.urls import path

from chat import views


app_name = "chat"

urlpatterns = [
    path("", views.chat, name="index"),
    path("update-contacts/", views.update_contacts, name="update_contacts"),
]
