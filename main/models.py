from django.db import models


class ContactUsMessage(models.Model):
    session_key = models.CharField(max_length=40)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact_us_messages"
        verbose_name = "Contact us message"
        verbose_name_plural = "Contact us messages"

    def __str__(self):
        return f"Message from {self.name} at {self.created_at}"
