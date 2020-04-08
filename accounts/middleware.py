from django.shortcuts import redirect
from django.conf import settings


class UserAthenticateRedirect(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # check if user is not athenticated then redirect him to login page
        # print(f'equality of ({request.path}) and ({settings.LOGIN_URL}) is {request.path != settings.LOGIN_URL}')
        if not request.user.is_authenticated and (request.path != settings.LOGIN_URL):
            print('user is not here')
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response
