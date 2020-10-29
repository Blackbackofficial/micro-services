from django.contrib import admin
from django.urls import path, include
from django_openapi import OpenAPI
from django_openapi import Path, Query, Form
from rest_framework.schemas import get_schema_view

# create an API object instance
api = OpenAPI(title='My OpenAPI Test', prefix_path='/test_api')

API_VERSION = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION + 'store/', include("store.urls")),
    path('manage/health/', include('store.health_url')),
    path('api-docs', get_schema_view(title="Store", description="Store service", version="1.0.0", public=True)),
    api.as_django_url_pattern()  # Add API object into urlpatterns
]


@api.get('/test/hello_via_path/{word}', tags=['test'])
def hello_via_path(word=Path()):
    return {'hello': word}
