from django.db import models
from django.db.models import Q


class Message(models.Model):
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="sent_messages",
        related_query_name="sent_messages",
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="received_messages",
        related_query_name="received_messages",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.created_at}"

    def to_dict(self):
        """
        Convert the Message instance into a dictionary.
        """
        return {
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
        }


def get_user_messages(user):
    """
    Get all messages related to a user (either sent or received).
    """
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
    return [message.to_dict() for message in messages]
