from django.urls import path
from . import views

urlpatterns = [
    # path('<str:orderItemUid>/warranty', views.warranty_solution),
    path('', views.post_items),
    path('<str:orderItemUid>', views.request_items),
    path('<str:orderItemUid>/warranty', views.request_warranty)
]
