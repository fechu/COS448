from django.contrib.auth.models import User
from django.db import models


class Business(models.Model):
    """
    A business on our page that can create offers.

    Attributes:
        user        The user that claimed this business.
        yelp_id     The id of the business on yelp.
        longitude   The longitude part of the location.
        latitude    The latitude part of the location.
    """

    yelp_id = models.TextField()
    name = models.TextField()
    url = models.URLField()

    longitude = models.FloatField()
    latitude = models.FloatField()

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='businesses'
    )

    def __str__(self):
        return self.name


class Offer(models.Model):
    """
    An offer created by a individual or a company to offer their food.

    Attributes:
        user        The user who created this offer.
        text        The text the offer should contain.
        business    An optional business for which the offer is.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offers'
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='offers',
        null=True
    )

    text = models.TextField(max_length=300)
