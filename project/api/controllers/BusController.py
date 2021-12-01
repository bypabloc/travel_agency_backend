from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.BusRepository import BusListForm, BusCreateForm, BusFindOneForm, BusStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        buses = BusListForm()
        buses.request = request
        data['buses'] = buses.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        bus = BusFindOneForm()
        bus.request = request
        if bus.is_valid():
            data['bus'] = bus.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=bus.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        bus = BusCreateForm(request.POST)

        if bus.is_valid():
            data['bus'] = bus.save()
            return sendCreated(data=data)
        else:
            return sendUnprocessableEntity(errors=bus.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        bus = BusStateChangeForm(request.POST)

        if bus.is_valid():
            data['bus'] = bus.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=bus.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
