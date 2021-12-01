from rest_framework.response import Response
from rest_framework import status

def sendSuccess(data = {}, message = []):
    try:
        return Response({
            'data': data,
            'message': message,
        }, status=status.HTTP_200_OK)
    except Exception as ex:
        return sendInternalServerError(ex)

def sendCreated(data = {}, message = []):
    try:
        return Response({
            'data': data,
            'message': message,
        }, status=status.HTTP_201_CREATED)
    except Exception as ex: lambda ex : sendInternalServerError(ex)

def sendUnprocessableEntity(errors = []):
    try:
        return Response({
            'errors': errors,
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as ex: lambda ex : sendInternalServerError(ex)

def sendInternalServerError(ex):
    print('sendInternalServerError -> ex',ex)
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
