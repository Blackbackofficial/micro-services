from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

API_VERSION = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION+'orders/', include("orders.urls")),
    path('manage/health/', include('orders.health_url')),
    path('api-docs/', get_swagger_view(title='Orders API'))
]
