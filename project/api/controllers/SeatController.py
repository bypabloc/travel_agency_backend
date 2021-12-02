from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.SeatRepository import SeatListForm, SeatCreateForm, SeatFindOneForm, SeatStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        seats = SeatListForm()
        seats.request = request
        data['seats'] = seats.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        seat = SeatFindOneForm()
        seat.request = request
        if seat.is_valid():
            data['seat'] = seat.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=seat.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        message = ['Seat created successfully']
        
        seat = SeatCreateForm(request.POST)

        if seat.is_valid():
            data['seat'] = seat.save()
            return sendCreated(data=data, message=message)
        else:
            return sendUnprocessableEntity(errors=seat.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        seat = SeatStateChangeForm(request.POST)

        if seat.is_valid():
            data['seat'] = seat.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=seat.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
