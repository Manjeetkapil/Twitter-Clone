from django.conf.urls import include
from django.urls import path
from .views import index, room

urlpatterns = [
    path('', index, name='index'),
    path('<slug:room_name>/', room, name='room'),
]
