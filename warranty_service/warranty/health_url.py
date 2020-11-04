from django.urls import path
from warranty_service.warranty.migrations.health import HealthCheckCustom

urlpatterns = [
    path('', HealthCheckCustom.as_view())
]
