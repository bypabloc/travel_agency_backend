from django.urls import path, include

urlpatterns = [
    path('bus/', include('app.routes.BusRoutes')),
    path('driver/', include('app.routes.DriverRoutes')),
    path('location/', include('app.routes.LocationRoutes')),
    path('journey/', include('app.routes.JourneyRoutes')),
    path('passenger/', include('app.routes.PassengerRoutes')),
    path('seat/', include('app.routes.SeatRoutes')),
    path('journey_driver/', include('app.routes.JourneyDriverRoutes')),
    path('ticket/', include('app.routes.TicketRoutes')),
    
]
