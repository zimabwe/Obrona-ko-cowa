from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import PacjentRegistrationForm,  DietForm, PanelDietetykaForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Feedback, Wizyta, Diet
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse
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
    feedbacks = Feedback.objects.filter(patient=user)

    if feedbacks.exists():
        feedback = feedbacks.first()  # lub dowolny inny sposób dostępu do obiektów, które pasują
    else:
        feedback = Feedback.objects.create(patient=user, comment='')

    if request.method == 'POST':
        uwagi = request.POST.get('uwagi', '')
        feedback.comment = uwagi
        feedback.save()

    wizyty = Wizyta.objects.filter(patient=user)
    diety = Diet.objects.filter(patient=user)

    return render(request, 'panel_pacjenta.html', {'feedback': feedback, 'wizyty': wizyty, 'diety': diety})

@login_required
def pobierz_diete(request, diet_id):
    diet = get_object_or_404(Diet, id=diet_id)
    response = HttpResponse(diet.pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{diet.pdf_file.name}"'
    return response



def panel_dietetyka(request):
    if request.method == 'POST':
        pacjent_id = request.POST.get('pacjent_id')
        informacje_wizytowe = request.POST.get('informacje_wizytowe', '')
        user = request.user

        if user.is_staff:
            wizyta = Wizyta.objects.create(patient_id=pacjent_id, date=datetime.date.today(), description=informacje_wizytowe)

            # Utwórz najpierw obiekt Feedback
            feedback = Feedback.objects.create(patient_id=pacjent_id, comment='')

            diet_form = DietForm(request.POST, request.FILES)
            if diet_form.is_valid():
                plik_pdf = diet_form.cleaned_data['plik_pdf']
                # Użyj obiektu Feedback do utworzenia obiektu Diet
                Diet.objects.create(patient_id=pacjent_id, plik_pdf=plik_pdf, feedback=feedback)

        return redirect('panel_dietetyka')

    pacjenci = User.objects.filter(is_staff=False)
    feedbacks = Feedback.objects.filter(patient__in=pacjenci)
    diet_form = DietForm()

    return render(request, 'panel_dietetyka.html', {'pacjenci': pacjenci, 'feedbacks': feedbacks, 'diet_form': diet_form})




@login_required
def strona_glowna(request):
    return render(request, 'base.html')