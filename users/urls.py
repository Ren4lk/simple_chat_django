from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path("", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.logout, name="logout"),
    path("edit/", views.edit, name="edit"),
]
