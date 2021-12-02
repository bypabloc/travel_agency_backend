from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.JourneyRepository import JourneyListForm, JourneyCreateForm, JourneyFindOneForm, JourneyStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        journeys = JourneyListForm()
        journeys.request = request
        data['journeys'] = journeys.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        journey = JourneyFindOneForm()
        journey.request = request
        if journey.is_valid():
            data['journey'] = journey.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journey.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        message = ['Journey created successfully']
        
        journey = JourneyCreateForm(request.POST)

        if journey.is_valid():
            data['journey'] = journey.save()
            return sendCreated(data=data, message=message)
        else:
            return sendUnprocessableEntity(errors=journey.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        journey = JourneyStateChangeForm(request.POST)

        if journey.is_valid():
            data['journey'] = journey.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journey.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
