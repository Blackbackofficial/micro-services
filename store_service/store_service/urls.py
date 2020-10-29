from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Store API')

API_VERSION = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION + 'store/', include("store.urls")),
    path('manage/health/', include('store.health_url')),
    path('api-docs/', schema_view)
]
