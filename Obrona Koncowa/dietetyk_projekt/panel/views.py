from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PacjentRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
def base(request):
    return render(request, 'base.html')

def register_pacjent(request):
    if request.method == 'POST':
        form = PacjentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PacjentRegistrationForm()

    return render(request, 'register_pacjent.html', {'form': form})

def login_pacjent(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # zmienić później na stronę panelu pacjenta
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

