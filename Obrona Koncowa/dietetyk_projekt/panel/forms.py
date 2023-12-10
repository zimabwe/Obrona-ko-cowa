from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Diet


class PacjentRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Wprowadź prawidłowy adres e-mail.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PacjentLoginForm(AuthenticationForm):

    pass


class PanelPacjentaForm(forms.Form):
    uwagi = forms.CharField(widget=forms.Textarea)

class PanelDietetykaForm(forms.Form):
    informacje_wizytowe = forms.CharField(widget=forms.Textarea)
    plik_pdf = forms.FileField(required=False)
    button_submit = forms.CharField(widget=forms.HiddenInput(), initial='')

    def __init__(self, *args, **kwargs):
        super(PanelDietetykaForm, self).__init__(*args, **kwargs)
        self.fields['button_submit'].widget.attrs['class'] = 'hidden'  # ukrywamy to pole, ale zostawić je w formularzu

    def clean(self):
        cleaned_data = super(PanelDietetykaForm, self).clean()
        if 'button_submit' in self.data:
            # Plik PDF nie jest obowiązkowy tylko wtedy, gdy zostanie naciśnięty przycisk zapisu bez wybrania pliku
            if not cleaned_data.get('plik_pdf'):
                self._errors['plik_pdf'] = self.error_class(['To pole jest wymagane.'])
        return cleaned_data


class DietForm(forms.ModelForm):
    class Meta:
        model = Diet
        fields = ['pdf_file']

