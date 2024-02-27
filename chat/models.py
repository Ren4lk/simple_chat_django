from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='receiver', null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)