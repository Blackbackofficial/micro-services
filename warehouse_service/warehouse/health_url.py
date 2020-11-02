from CustomHealthCheck.HelthCheck import HealthCheckCustom
from django.urls import path


urlpatterns = [
    path('', HealthCheckCustom.as_view())
]
