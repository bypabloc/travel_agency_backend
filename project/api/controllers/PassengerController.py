from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.PassengerRepository import PassengerListForm, PassengerCreateForm, PassengerFindOneForm, PassengerStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        passengers = PassengerListForm()
        passengers.request = request
        data['passengers'] = passengers.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        passenger = PassengerFindOneForm()
        passenger.request = request
        if passenger.is_valid():
            data['passenger'] = passenger.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=passenger.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        message = ['Passenger created successfully']
        
        passenger = PassengerCreateForm(request.POST)

        if passenger.is_valid():
            data['passenger'] = passenger.save()
            return sendCreated(data=data, message=message)
        else:
            return sendUnprocessableEntity(errors=passenger.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        passenger = PassengerStateChangeForm(request.POST)

        if passenger.is_valid():
            data['passenger'] = passenger.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=passenger.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
