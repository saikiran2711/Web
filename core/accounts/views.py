from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import Form
from django.contrib.auth.models import User



# Create your views here.

def register(request):
    form = Form()
    if request.method == "POST":

        form = Form(request.POST)
        try:
            a=User.objects.get_by_natural_key(username=request.POST.get('username'))
        except User.DoesNotExist:
            if form.is_valid():
                    form.save()
                    return redirect('login')
            else:
                print("Not validated")
                messages.error(request, "Enter Details correctly")
                return redirect('register')
        messages.error(request, "User with this user name already exists!!")
        return redirect('register')
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    if  request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User Not found !")
            return redirect('login')
    return render(request,"login.html")
