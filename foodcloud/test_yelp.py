from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key="uz2Sv5gO6dwlnjRv3BqzwA",
    consumer_secret="VhgG3IucBO_eTheOlWzrVuuVjbU",
    token="bN1HD9FSDGqUWjzxbIkho_N1muVe0xcA",
    token_secret="hEdALK5D2gCI9-H3GwGKAw1jEYo"
)

client = Client(auth)

response = client.get_business('d-angelo-italian-market-princeton')
print(response.business.location.coordinate.latitude)
print(response.business.location.coordinate.longitude)
