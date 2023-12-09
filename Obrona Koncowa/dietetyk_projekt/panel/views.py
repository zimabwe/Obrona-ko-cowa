from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PacjentRegistrationForm,  DietForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Feedback, Wizyta, Diet
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime

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

            if user.is_staff:
                return redirect('panel_dietetyka')
            else:
                return redirect('panel_pacjenta')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
User = get_user_model()

@login_required
def panel_pacjenta(request):
    user = request.user
    feedback, created = Feedback.objects.get_or_create(patient=user)

    if request.method == 'POST':
        uwagi = request.POST.get('uwagi', '')
        feedback.comment = uwagi
        feedback.save()

    wizyty = Wizyta.objects.filter(patient=user)

    return render(request, 'panel_pacjenta.html', {'feedback': feedback, 'wizyty': wizyty})



def panel_dietetyka(request):
    if request.method == 'POST':
        pacjent_id = request.POST.get('pacjent_id')
        informacje_wizytowe = request.POST.get('informacje_wizytowe', '')
        user = request.user

        if user.is_staff:
            wizyta = Wizyta.objects.create(patient_id=pacjent_id, date=datetime.date.today(), description=informacje_wizytowe)


            diet_form = DietForm(request.POST, request.FILES)
            if diet_form.is_valid():
                pdf_file = diet_form.cleaned_data['pdf_file']
                Diet.objects.create(patient_id=pacjent_id, pdf_file=pdf_file, feedback=wizyta)

        return redirect('panel_dietetyka')

    pacjenci = User.objects.filter(is_staff=False)
    feedbacks = Feedback.objects.filter(patient__in=pacjenci)
    diet_form = DietForm()  # Dodane: Inicjalizacja formularza do dodawania diety

    return render(request, 'panel_dietetyka.html', {'pacjenci': pacjenci, 'feedbacks': feedbacks, 'diet_form': diet_form})


@login_required
def strona_glowna(request):
    return render(request, 'base.html')