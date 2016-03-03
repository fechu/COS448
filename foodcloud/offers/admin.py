from django.contrib import admin
from offers.models import Offer


class OfferAdmin(admin.ModelAdmin):
    pass

admin.site.register(Offer, OfferAdmin)

