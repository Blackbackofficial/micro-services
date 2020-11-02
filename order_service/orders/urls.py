from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_uid>', views.actions_orders, name='make_orders'),
    path('<str:user_uid>/<str:order_uid>', views.one_order, name='one_order'),
    path('<str:user_uid>/<str:order_uid>/warranty', views.warranty_order, name='warranty_order'),
]
