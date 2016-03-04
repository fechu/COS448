from offers.models import Business, Device, Region
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from geopy.distance import great_circle


class YelpService(object):

    def __init__(self):
        auth = Oauth1Authenticator(
            consumer_key="uz2Sv5gO6dwlnjRv3BqzwA",
            consumer_secret="VhgG3IucBO_eTheOlWzrVuuVjbU",
            token="bN1HD9FSDGqUWjzxbIkho_N1muVe0xcA",
            token_secret="hEdALK5D2gCI9-H3GwGKAw1jEYo"
        )

        self.client = Client(auth)

        self._business_cache = {}

    def get_location(self, yelp_id):
        """
        Get the location of a yelp business
        """
        business = self._get_business(yelp_id)
        return business.location.coordinate

    def get_name(self, yelp_id):
        """
        Get the name of a location
        """
        business = self._get_business(yelp_id)
        return business.name

    def get_url(self, yelp_id):
        """
        Get the url to the yelp side of a business
        """
        business = self._get_business(yelp_id)
        return business.url

    def _get_business(self, yelp_id):
        if yelp_id in self._business_cache:
            return self._business_cache[yelp_id]
        else:
            response = self.client.get_business(yelp_id)
            self._business_cache[yelp_id] = response.business
            return response.business

    def search(self, query, location):
        response = self.client.search(location=location, term=query)
        return response.businesses


class BusinessService(object):
    """
    A class providing methods to interact with businesses
    """

    def create_business(self, yelp_id):
        """
        Create a new business from a yelp id.
        This method tries to gather additional information from yelp.
        Args:
            yelp_id: The yelp id for which to create a business

        Returns: The created business

        """
        business = Business()
        business.yelp_id = yelp_id

        # Gather additional information
        yelp_service = YelpService()
        location = yelp_service.get_location(yelp_id)
        business.latitude = location.latitude
        business.longitude = location.longitude
        business.url = yelp_service.get_url(yelp_id)

        business.name = yelp_service.get_name(yelp_id)

        return business


class DeviceService(object):
    """
    Provides serveral services for devices.
    """

    def devices_for_offer(self, offer):
        """
        Get all devices that fullfill all the requirements for an offer.
        Args:
            offer (Offer): The offer for which you want all devices.

        Returns: A list of devices.

        """
        devices = []

        offer_location = offer.get_location()
        regions = Region.objects.all()
        for region in regions:
            distance = great_circle(offer_location, region.get_location()).meters

            # Both, the offer and the user must be in range of each other.
            if distance <= region.range and distance <= offer.range:
                devices.append(region.device)

        return devices




