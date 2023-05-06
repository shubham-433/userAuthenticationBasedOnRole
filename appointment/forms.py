from django import forms

from .models import Appointment

class AppointmentForm(forms.ModelForm):
    
        geeks_field = forms.DateTimeField( )
