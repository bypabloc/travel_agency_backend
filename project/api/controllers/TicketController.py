from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.TicketRepository import TicketListForm, TicketCreateForm, TicketFindOneForm, TicketStateChangeForm, TicketSeatChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        tickets = TicketListForm()
        tickets.request = request
        data['tickets'] = tickets.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        ticket = TicketFindOneForm()
        ticket.request = request
        if ticket.is_valid():
            data['ticket'] = ticket.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=ticket.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        ticket = TicketCreateForm(request.data)
        ticket.request = request

        if ticket.is_valid():
            data['ticket'] = ticket.save()
            return sendCreated(data=data)
        else:
            return sendUnprocessableEntity(errors=ticket.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        ticket = TicketStateChangeForm(request.data)

        if ticket.is_valid():
            data['ticket'] = ticket.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=ticket.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['POST'])
@csrf_exempt
def seat_change(request):
    try:
        data = {}
        ticket = TicketSeatChangeForm(request.data)

        if ticket.is_valid():
            data['ticket'] = ticket.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=ticket.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)

