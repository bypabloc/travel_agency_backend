from django.urls import path, include

urlpatterns = [
    path('bus/', include('api.routes.bus')),
]