from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.LocationRepository import LocationListForm, LocationCreateForm, LocationFindOneForm, LocationStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        locations = LocationListForm()
        locations.request = request
        data['locations'] = locations.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        location = LocationFindOneForm()
        location.request = request
        if location.is_valid():
            data['location'] = location.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=location.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        location = LocationCreateForm(request.data)

        if location.is_valid():
            data['location'] = location.save()
            return sendCreated(data=data)
        else:
            return sendUnprocessableEntity(errors=location.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        location = LocationStateChangeForm(request.data)

        if location.is_valid():
            data['location'] = location.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=location.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
