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
        text                The text the offer should contain.
        business            An optional business for which the offer is.
        user                The user who created this offer.
        push_notifications  Push notifications already sent?
        range               The range in which push notifications should be sent in meters.
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
    push_notifications = models.BooleanField(default=False)
    range = models.PositiveIntegerField(default=3000)

    # All the devices that got a push notification of this offer.
    devices = models.ManyToManyField('Device', related_name="offers", blank=True)

    def get_location(self):
        """
        Get the location of this offer. This is the same as the location of the business.
        Returns:
            The location of the offer.
        """
        return self.business.latitude, self.business.longitude


class AppUser(models.Model):
    """
    A user of our app.
    """

    email = models.EmailField()


class Device(APNSDevice):
    """
    A device that we use in this application. Each device can have multiple regions attached.
    """

    app_user = models.ForeignKey(AppUser)

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

    def get_location(self):
        """
        Get the location of this region as a tuple.
        """
        return self.latitude, self.longitude

    def __str__(self):
        return "(%f, %f, %d m)" % (self.latitude, self.longitude, self.range)








