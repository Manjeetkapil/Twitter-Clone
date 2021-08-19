# chat/views.py
from django.shortcuts import render
from .models import Room


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    messages = Room.objects.all().filter(key=room_name)
    print(messages)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chat': messages
    })
