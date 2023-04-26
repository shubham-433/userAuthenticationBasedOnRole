from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from .models import CustomUser
# forms

class RegistrationForm(UserCreationForm):
   
    is_doctor = forms.BooleanField(required=False,  widget=forms.CheckboxInput(attrs={'class':'form-check-input form-control'}))
    # profilePic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    profilePic=forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email','is_doctor' ,'profilePic' )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            
         
            }


class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password =forms.CharField(label='password',widget= forms.PasswordInput(attrs={'class':'form-control'}))