from django.contrib import admin
from django.urls import path, include

API_VERSION = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION+'store/', include("store.urls")),
    path('manage/health/', include('store.health_url')),
]
