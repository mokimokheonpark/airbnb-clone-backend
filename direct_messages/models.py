from django.db import models
from common.models import CommonModel


# Message Room Model Definition
class MessageRoom(CommonModel):
    def __str__(self) -> str:
        return "Message Room"

    users = models.ManyToManyField(
        "users.User",
        related_name="message_rooms",
    )


# Message Model Definition
class Message(CommonModel):
    def __str__(self) -> str:
        return f"{self.user}: {self.text}"

    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )

    text = models.TextField()

    room = models.ForeignKey(
        "direct_messages.MessageRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
