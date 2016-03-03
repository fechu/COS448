from offers.models import Business
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


class YelpService(object):

    def __init__(self):
        auth = Oauth1Authenticator(
            consumer_key="uz2Sv5gO6dwlnjRv3BqzwA",
            consumer_secret="VhgG3IucBO_eTheOlWzrVuuVjbU",
            token="bN1HD9FSDGqUWjzxbIkho_N1muVe0xcA",
            token_secret="hEdALK5D2gCI9-H3GwGKAw1jEYo"
        )

        self.client = Client(auth)

    def get_location(self, yelp_id):
        """
        Get the location of a yelp business
        """
        response = self.client.get_business(yelp_id)
        return response.business.location.coordinate

    def get_name(self, yelp_id):
        """
        Get the name of a location
        """
        response = self.client.get_business(yelp_id)
        return response.business.name


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

        business.name = yelp_service.get_name(yelp_id)

        return business



