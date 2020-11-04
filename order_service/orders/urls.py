from django.urls import path
from . import views

urlpatterns = [
    path('<str:order_uid>/warranty', views.warranty_order),
    path('<str:user_uid>', views.actions_orders),
    path('<str:user_uid>/<str:order_uid>', views.one_order),
    # path('<str:order_uid>/warranty', views.warranty_order)
]
