from django.urls import path
from ..controllers.JourneyDriverController import list, findOne, create, state_change, driver_change

urlpatterns = [
    path('list', list, name='list'),
    path('find_one', findOne, name='findOne'),
    path('create', create, name='create'),
    path('state_change', state_change, name='state_change'),
    path('driver_change', driver_change, name='driver_change'),
]
