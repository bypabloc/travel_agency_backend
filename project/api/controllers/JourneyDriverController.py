from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.JourneyDriverRepository import JourneyDriverListForm, JourneyDriverCreateForm, JourneyDriverFindOneForm, JourneyDriverStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        journeysdrivers = JourneyDriverListForm()
        journeysdrivers.request = request
        data['journeysdrivers'] = journeysdrivers.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        journeydriver = JourneyDriverFindOneForm()
        journeydriver.request = request
        if journeydriver.is_valid():
            data['journeydriver'] = journeydriver.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journeydriver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        journeydriver = JourneyDriverCreateForm(request.POST)

        if journeydriver.is_valid():
            data['journeydriver'] = journeydriver.save()
            return sendCreated(data=data)
        else:
            return sendUnprocessableEntity(errors=journeydriver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        journeydriver = JourneyDriverStateChangeForm(request.POST)

        if journeydriver.is_valid():
            data['journeydriver'] = journeydriver.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=journeydriver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
