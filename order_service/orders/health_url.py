from django.urls import path
from . import health

urlpatterns = [
    path('', health.HealthCheckCustom.as_view())
]
