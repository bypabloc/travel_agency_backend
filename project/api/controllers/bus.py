from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

@api_view(['GET'])
@csrf_exempt
def list(request):

    return Response({}, status=status.HTTP_201_CREATED)
    user = AuthSignUpForm(request.POST)

    if user.is_valid():
        user.save()
        data = {
            'data': user.cleaned_data,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            'errors': user.getErrors(),
        }
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
