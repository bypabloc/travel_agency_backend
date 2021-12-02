from django.urls import path, include

urlpatterns = [
    path('bus/', include('api.routes.BusRoutes')),
    path('driver/', include('api.routes.DriverRoutes')),
    path('location/', include('api.routes.LocationRoutes')),
    path('journey/', include('api.routes.JourneyRoutes')),
    path('passenger/', include('api.routes.PassengerRoutes')),
    path('seat/', include('api.routes.SeatRoutes')),
    path('journey_driver/', include('api.routes.JourneyDriverRoutes')),
]
