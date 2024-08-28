from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form_register = UserForm(request.POST)
        if form_register.is_valid():
            user = form_register.save(commit=False)
            user.set_password(user.password)
            form_register.save()
            return redirect('home')
        else:
            return redirect('register')
    else:
        form_register = UserForm()
    return render(request, 'register.html', {'form_register': form_register})

def auth(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password:
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли!')
                    return redirect('home')
                else:
                    messages.error(request, "Неверный логин или пароль!")
            except Exception as ex:
                messages.error(request, "Призошла ошибка при аутентификации. Пожалуйста, попробуйте снова")
        else:
            messages.warning(request, 'Заполните все поля!')
    return render(request, 'auth.html')

def exit(request):
    logout(request)
    messages.success(request, "Вы успешно вышли!")
    return redirect('home')
