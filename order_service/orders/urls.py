from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_uid>', views.make_orders, name='make_orders'),
    path('<str:user_uid>/<str:order_uid>', views.one_order, name='one_order'),
    # path('<str:user_uid>/<str:order_uid>/warranty', views.get_order_warranty, name='get_order_warranty'),
    # path('<str:user_uid>/<str:order_uid>/refund', views.get_order_refund, name='get_order_refund'),
]
