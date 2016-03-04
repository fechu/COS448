from django.conf.urls import url
from offers.api.views import post_device

urlpatterns = [
    url(r'^devices/', post_device)
]