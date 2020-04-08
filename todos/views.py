from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm

@login_required
def todos(request):
    todo_list = Todo.objects.all()
    data = {
        'todos': list(todo_list.values(
            'todo', 'done'
        ))
    }
    return JsonResponse(data)

@login_required
def todos_details(request, id):
    todo = get_object_or_404(Todo, pk=id)
    data = {
        'todo': todo.todo,
        'done': todo.done,
    }
    return JsonResponse(data)

@login_required
def add_todo(request):
    if request.method == 'POST':
        todo = Todo(
            todo = request.POST['todo'],
        )
        print('i will get this todo saved to db', todo.todo, todo.done)
        todo.save()
        return redirect('/todo/list')
    else:
        form = TodoForm()
        return render(request, 'todos/add_todo.html', {'form': form})
