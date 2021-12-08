from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from ..repository.DriverRepository import DriverListForm, DriverCreateForm, DriverFindOneForm, DriverStateChangeForm
from ..helpers.response import sendSuccess, sendCreated, sendUnprocessableEntity, sendInternalServerError

@api_view(['GET'])
@csrf_exempt
def list(request):
    try:
        data = {}
        drivers = DriverListForm()
        drivers.request = request
        data['drivers'] = drivers.list()

        return sendSuccess(data=data)
    except Exception as ex:
        return sendInternalServerError(ex=ex)

@api_view(['GET'])
@csrf_exempt
def findOne(request):
    try:
        data = {}
        driver = DriverFindOneForm()
        driver.request = request
        if driver.is_valid():
            data['driver'] = driver.find()
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
        
@api_view(['POST'])
@csrf_exempt
def create(request):
    try:
        data = {}
        message = ['Driver created successfully']
        
        driver = DriverCreateForm(request.data)

        if driver.is_valid():
            data['driver'] = driver.save()
            return sendCreated(data=data, message=message)
        else:
            return sendUnprocessableEntity(errors=driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)


@api_view(['POST'])
@csrf_exempt
def state_change(request):
    try:
        data = {}
        driver = DriverStateChangeForm(request.data)

        if driver.is_valid():
            data['driver'] = driver.save()
            print('data', data)
            return sendSuccess(data=data)
        else:
            return sendUnprocessableEntity(errors=driver.getErrors())
    except Exception as ex:
        return sendInternalServerError(ex=ex)
