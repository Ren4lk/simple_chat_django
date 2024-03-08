from django.db import models
from django.db.models import Q

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='receiver', null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'sender': self.sender.username if self.sender else None,
            'receiver': self.receiver.username if self.receiver else None,
            'text': self.text,
            'created_at': self.created_at.isoformat()
        }


def get_user_messages(user):
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
    return [message.to_dict() for message in messages]