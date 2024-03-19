from django.contrib import admin

from main.models import ContactUsMessage


@admin.register(ContactUsMessage)
class ContactUsMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "created_at")
