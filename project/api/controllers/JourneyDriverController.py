from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.JourneyDriverRepository import JourneyDriverListForm, JourneyDriverCreateForm, JourneyDriverFindOneForm, JourneyDriverStateChangeForm, JourneyDriverChangeDriverForm, JourneyDriverJourneysForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        journeys_drivers = JourneyDriverListForm()
        journeys_drivers.request = request
        data['journeys_drivers'] = journeys_drivers.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        journey_driver = JourneyDriverFindOneForm()
        journey_driver.request = request
        if journey_driver.is_valid():
            data['journey_driver'] = journey_driver.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journey_driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        journey_driver = JourneyDriverCreateForm(request.data)
        journey_driver.request = request

        if journey_driver.is_valid():
            data['journey_driver'] = journey_driver.save()
            return sendCreated(data=data)
        else:
            return sendUnprocessableEntity(errors=journey_driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        journey_driver = JourneyDriverStateChangeForm(request.data)

        if journey_driver.is_valid():
            data['journey_driver'] = journey_driver.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journey_driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['POST'])
@csrf_exempt
def driver_change(request):
    try:
        data = {}
        journey_driver = JourneyDriverChangeDriverForm(request.data)

        if journey_driver.is_valid():
            data['journey_driver'] = journey_driver.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journey_driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def journeys(request):
    try:
        data = {}
        journeys_drivers = JourneyDriverJourneysForm()
        journeys_drivers.request = request
        if journeys_drivers.is_valid():
            data['journeys_drivers'] = journeys_drivers.list()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journeys_drivers.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)

