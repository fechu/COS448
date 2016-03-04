from django.conf.urls import url
from offers.api.views import post_device, post_regions



urlpatterns = [
    url(r'^devices/(?P<device_token>[\w]+)/regions/', post_regions),
    url(r'^devices/', post_device),
]