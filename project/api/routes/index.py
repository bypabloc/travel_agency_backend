from django.urls import path, include

urlpatterns = [
    path('bus/', include('api.routes.BusRoutes')),
    path('driver/', include('api.routes.DriverRoutes')),
]