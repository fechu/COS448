import json

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from offers.models import Region, Device, AppUser
from django.views.decorators.csrf import csrf_exempt


@require_POST
@csrf_exempt
def post_device(request):
    """
    Post a device (push notification) identifier with an email to create a new entry.

    Args:
        request (HttpRequest): The request from the user.
    """

    # Parse the body.
    raw_data = request.body.decode('utf-8')
    if raw_data is None or raw_data == '':
        return HttpResponseBadRequest()

    data = json.loads(raw_data)
    if data is None:
        return HttpResponseBadRequest()

    if not _deserialize_device_request(data):
        return HttpResponseBadRequest()

    return HttpResponse(status=201)


@require_POST
@csrf_exempt
def post_regions(request, device_token):
    """
    Takes a json object containing regions and adds them to a device.

    Args:
        request (HttpRequest):
    """
    device = get_object_or_404(Device, registration_id=device_token)
    # Delete all old regions from that device
    Region.objects.filter(device=device).delete()

    # Parse the body.
    raw_data = request.body.decode('utf-8')
    if raw_data is None or raw_data == '':
        return HttpResponseBadRequest()

    data = json.loads(raw_data)
    if data is None:
        return HttpResponseBadRequest()
    regions_data = data.get('regions', None)
    if regions_data is None:
        return HttpResponseBadRequest()

    result = _deserialize_regions(regions_data)
    if result is False:
        return HttpResponseBadRequest()

    for region in result:
        region.device = device
        region.save()

    return HttpResponse(status=201)


def _deserialize_device_request(data):
    """
    Takes a json string and tries to decode it to get a device identifier, email and a list of regions.

    Args:
        data (dict): 
    """
    device_token = data.get('device_token', None)
    email = data.get('email', None)

    if device_token is None or email is None:
        return False

    user, created = AppUser.objects.get_or_create(email=email)

    device, created = Device.objects.get_or_create(registration_id=device_token, defaults={'app_user': user})
    device.app_user = user
    device.save()

    return True


def _deserialize_regions(regions):
    # Check the regions
    region_objects = []
    for region in regions:
        long = region.get('longitude', None)
        lat = region.get('latitude', None)
        range = region.get('range', None)
        if long is None or lat is None or range is None:
            return False

        region_object = Region(latitude=lat, longitude=long, range=range)
        region_objects.append(region_object)

    return region_objects





