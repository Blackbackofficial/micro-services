from django.urls import path
from . import views


urlpatterns = [
    path('', views.HealthCheckCustom.as_view(), name='health_check_custom'),
]
