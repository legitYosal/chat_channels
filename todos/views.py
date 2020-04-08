from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo

@login_required
def todos(request):
    todo_list = Todo.objects.all()
    data = {
        'todos': list(todo_list.values(
            'todo', 'done'
        ))
    }
    return JsonResponse(data)

def todos_details(request, id):
    todo = get_object_or_404(Todo, pk=id)
    data = {
        'todo': todo.todo,
        'done': todo.done,
    }
    return JsonResponse(data)
