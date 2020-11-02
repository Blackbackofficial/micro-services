from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

API_VERSION = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION + 'warranty/', include("warranty.urls")),
    path('manage/health/', include('warranty.health_url')),
    path('api-docs/', get_swagger_view(title='Warranty API'))
]
