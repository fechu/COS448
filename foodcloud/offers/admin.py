from django.contrib import admin
from offers.models import Offer, Business


class OfferAdmin(admin.ModelAdmin):
    pass

admin.site.register(Offer, OfferAdmin)


class BusinessAdmin(admin.ModelAdmin):
    pass

admin.site.register(Business, BusinessAdmin)

