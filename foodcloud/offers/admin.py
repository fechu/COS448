from commons.admin import CommonAdmin
from django.conf.urls import url
from django.contrib import admin
from django.core.checks import messages
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from offers.models import Offer, Business
from offers.services import YelpService, BusinessService


class OfferAdmin(CommonAdmin):
    show_add_button = False
    list_display = ['text', 'user', 'business']


admin.site.register(Offer, OfferAdmin)


class BusinessAdmin(CommonAdmin):
    show_add_button = False

    list_display = ['name', 'user', 'yelp_url']

    def yelp_url(self, obj):
        return '<a target="blank" href="' + obj.url + '">View on Yelp</a>'

    def create_offer_url(self, obj):
        return '<a target="blank" href="' + obj.url + '">View on Yelp</a>'


    yelp_url.allow_tags = True


    def get_button_actions(self):
        return [
            ('Add Business', reverse('admin:offers_business_select_yelp'))
        ]

    def get_urls(self):
        urls = super(BusinessAdmin, self).get_urls()

        additional_urls = [
            url(r'^select-business', self.select_yelp_business, name='offers_business_select_yelp'),
            url(r'^create-business', self.create_business, name='offers_business_create'),
        ]
        return additional_urls + urls

    def create_business(self, request):
        """
        Create a business from a business id.

        Args:
            request (HttpRequest):
        """
        business_id = request.GET.get('business_id', None)
        if business_id is None:
            return redirect('offers_business_add')

        business = BusinessService().create_business(business_id)
        business.user = request.user
        business.save()

        return redirect('admin:offers_business_changelist')

    def select_yelp_business(self, request):
        """
        First step in creating a business. Search and select a yelp business

        Args:
            request (HttpRequest):
        """

        context = {
            'title': 'Find your Business on Yelp',
        }

        if request.method == 'POST':

            query = request.POST.get('q', '')
            location = request.POST.get('loc', '')

            context['query'] = query
            context['location'] = location

            # Validation
            if query == '' or location == '':
                self.message_user(
                    request,
                    "Please provide the location and the name of your business.",
                    level=messages.WARNING
                )
            else:
                # Query the API
                response = YelpService().search(query, location)
                context['businesses'] = response

        return TemplateResponse(request, 'offers/select_yelp_business.html', context=context)


admin.site.register(Business, BusinessAdmin)
