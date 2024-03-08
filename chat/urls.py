# from django.urls import path

# from chat import views


# app_name = "chat"

# urlpatterns = [
#     path("", views.chat, name="index"),
#     path("update-contacts/", views.update_contacts, name="update_contacts"),
# ]


from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:target_user>/", views.index, name="index"),
    # path("<str:interlocutor_username>/", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),
]
