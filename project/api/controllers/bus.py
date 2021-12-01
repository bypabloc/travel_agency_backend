from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Lower
from rest_framework.response import Response
from ..helpers.pagination import paginate_queryset
from ..models import Bus

@api_view(['GET'])
@csrf_exempt
def list(request):
    data = {}
    try:
        queries = paginate_queryset(request)
        print('queries: ',queries)

        filters = {}

        buses = Bus.objects.filter(**filters)

        # buses = buses.raw("ORDER BY " + queries['sort_by'] + " " + queries['sort'])

        sort_by = queries['sort_by']
        buses = buses.extra(select={''+sort_by+'':'LOWER('+sort_by+')'})
        if queries['sort'] == 'asc':
            buses = buses.order_by(Lower(''+sort_by+'').asc())
        else:
            buses = buses.order_by(Lower(''+sort_by+'').desc())

        data['buses'] = buses

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

    return Response(data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@csrf_exempt
def findOne(request):

    return Response({}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
def create(request):
    
    return Response({}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
def state_change(request):
    
    return Response({}, status=status.HTTP_201_CREATED)
