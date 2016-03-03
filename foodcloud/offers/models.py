from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """
    An offer created by a individual or a company to offer their food.

    Attributes:
        user    The user who created this offer.
        text    The text the offer should contain.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offers'
    )

    text = models.TextField(max_length=300)
