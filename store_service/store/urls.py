from django.urls import path
from . import views


urlpatterns = [
    path('<str:user_uid>/orders', views.get_orders, name='getOrders'),
    # path('<str:user_uid>/<str:user>', StoreView.as_view()),
    path('<str:user_uid>/purchase', views.buy_order, name='buy_order')
]
