from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_items),
    path('<str:orderItemUid>', views.request_items),
    path('<str:orderItemUid>/warranty', views.request_warranty)
]
