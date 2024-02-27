from django.db import models


# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        db_table = "contact_messages"
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.name
