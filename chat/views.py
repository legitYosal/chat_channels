from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def lobby(request):
    return render(request, 'chat/lobby.html')

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@login_required
def index(request):
    return render(request, 'index/index.html')
