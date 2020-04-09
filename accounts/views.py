from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserLogin
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('user is posting')
        if user:
            login(request, user)
            # just make user online
            user.is_online = True
            user.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            # raise ValidationError(('user not exists'), code='invalid')
            return HttpResponse('login again')
    else:
        form = UserLogin()
        return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    request.user.is_online = False
    request.user.save()
    logout(request)
    return redirect(settings.LOGIN_URL)
