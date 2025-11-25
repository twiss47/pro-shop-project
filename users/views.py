# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('app:index')  

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone, password=password)

        if user:
            login(request, user)
            return redirect('app:index')  

        return render(request, 'users/login.html', {'error': 'Password or phone number is incorrect'})

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')  