from django.urls import path
from . import views

urlpatterns = [
    path('<str:item_uid>', views.actions_warranty),
    path('<str:item_uid>/warranty', views.request_warranty)
]
