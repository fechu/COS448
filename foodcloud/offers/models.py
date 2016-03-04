from django.contrib.auth.models import User
from django.db import models
from push_notifications.models import APNSDevice


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


class UserDevices(models.Model):
    """
    An extension to the user profile which adds devices and regions to the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_devices', null=True)


class Device(APNSDevice):
    """
    A device that we use in this application. Each device can have multiple regions attached.
    """

    user_devices = models.ForeignKey(UserDevices)

    def __str__(self):
        return self.registration_id


class Region(models.Model):
    """
    A region associated with a device in which the user of that device wants to receive notifications.

    Attributes:
        device:     The device to which this region belongs to.
        longitude:  Longitude of the region
        latitde:    Latitude of the region
        range:      The range from the center of this location in which the user wants to receive notifications.
                    This range is in meters.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    range = models.PositiveIntegerField()








