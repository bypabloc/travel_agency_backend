from django.urls import path
from ..controllers.SeatController import list, findOne, create, state_change, list_availability

urlpatterns = [
    path('list', list, name='list'),
    path('find_one', findOne, name='findOne'),
    path('create', create, name='create'),
    path('state_change', state_change, name='state_change'),
    path('list_availability', list_availability, name='list_availability'),
]
