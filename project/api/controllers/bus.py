from django.db.models import query
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination
from ..models import Bus
from ..repository.BusRepository import BusCreateForm, BusFindOneForm, BusStateChangeForm

@api_view(['GET'])
@csrf_exempt
def list(request):
    data = {}
    try:
        params = paginate_queryset(request)
        print('params: ',params)

        buses = Bus.objects

        buses = model_apply_filter(model=Bus, query=buses, params=params)
        buses = model_apply_sort(model=Bus, query=buses, params=params)
        buses = model_apply_pagination(query=buses, params=params)

        data['buses'] = buses

        return Response(data, status=status.HTTP_200_OK)

    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        
        data = {
            'status': 'error',
            'message': 'No hay datos',
            'trace': trace,
        }

        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@csrf_exempt
def findOne(request):

    bus = BusFindOneForm(paginate_queryset(request))

    if bus.is_valid():
        bus = bus.find()
        data = {
            'data': bus,
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {
            'errors': bus.getErrors(),
        }
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
@csrf_exempt
def create(request):

    bus = BusCreateForm(request.POST)

    if bus.is_valid():
        bus.save()
        data = {
            'data': bus.cleaned_data,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            'errors': bus.getErrors(),
        }
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
@csrf_exempt
def state_change(request):
    
    bus = BusStateChangeForm(request.POST)

    if bus.is_valid():
        bus.save()
        data = {
            'data': bus.cleaned_data,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            'errors': bus.getErrors(),
        }
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
