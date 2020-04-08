

from django.urls import path
from .views import todos, todos_details


urlpatterns = [
    path('list/', todos, name='todos'),
    path('list/<int:id>/', todos_details, name='todos_details'),
]
