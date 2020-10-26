from django.urls import path
from . import views
from .views import StoreView

urlpatterns = [
    # path('', views.index, name='main'),  # здесь мы переходим в функцию index в файле views
    # path('<int:pk>', views.index, name='main'),
    # path('about', views.about, name='about'),
    # path('create', views.create, name='create'),
    # path('persons/<int:pk>', views.up_del_person, name='up_del_person'),
    path('<str:user_uid>', StoreView.as_view()),
    path('<str:user_uid>/<str:user>', StoreView.as_view())
]
