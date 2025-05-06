from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, DatabaseError  # for errors
from .forms import TaskForm
from .models import Task

# import the timezone
from django.utils import timezone

# need to be login to access the view with a @declarator
from django.contrib.auth.decorators import login_required, login_not_required


"""
MAIN PAGE
============================================================
"""
# Create your views here. no login required
@login_not_required
def home(request):
    return render(request, 'home.html')


@login_not_required
def signup(request):
    if request.method == 'GET':
        print('get')
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        print('post')
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                # create the user
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                # return HttpResponse('User created successfully'.encode('utf-8'))

                # creamos una cookie para mantenernos en login
                login(request, user)

                # redirect to a new view
                return redirect('tasks')

            except IntegrityError as e:  # Catch the specific exception for username collision
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': f'That username is already taken. Please choose another: {e}'
                })
            except DatabaseError as e:  # Catch other potential database errors
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': f'Database error occurred: {e}'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Passwords do not match.'
            })


@login_not_required
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print('post')
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Invalid username and/or password.'
            })
        else:
            login(request, user)
            return redirect('tasks')


"""
VIEWS THAT WE CAN SEE  WHEN LOGIN
============================================================
"""
@login_required
def close_session(request):
    logout(request)
    return redirect('home')


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html',{
        'tasks': tasks,
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            # creamos un formulario y guardamos los datos de nuevo
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)

            # salvamos la data del usuatio
            new_task.user = request.user
            new_task.save()
            print(request.POST)
            return redirect('tasks')
        except ValueError as e:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': f'Please provide valide data: {e}'
            })


@login_required
def task_details(request, task_id):

    if request.method == 'GET':
        # busca dentro del objeto t ask el id dentro de las primekey y si no lo encuentra 404
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_details.html',{
            'task': task,
            'form': form
        })
    else:
        try:
            print(request.POST)
            # salvamos el formulario
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            update_data = TaskForm(request.POST, instance=task)
            update_data.save()
            return redirect('tasks')
        except ValueError as e:
            error = f'Error when updating the value: {e}'
            return render(request, 'task_details.html', {
                'task': task,
                'form': form,
                'error' : error
            })


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def finished_task(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'tasks.html',{
        'tasks': tasks,
    })



























