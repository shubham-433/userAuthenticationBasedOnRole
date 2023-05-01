from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from .models import CustomUser
from froala_editor.fields import FroalaField
from froala_editor.widgets import FroalaEditor
from .models import *
# forms

class RegistrationForm(UserCreationForm):
   
    is_doctor = forms.BooleanField(required=False,  widget=forms.CheckboxInput(attrs={'class':'form-check-input form-control'}))
    # profilePic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    address=forms.CharField(label="address",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address','rows':3}))
    

    profilePic=forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email','is_doctor' ,'profilePic','address' )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            
         
            }


class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password =forms.CharField(label='password',widget= forms.PasswordInput(attrs={'class':'form-control'}))



# blog form

class AddBlogForm(forms.ModelForm):
    # Alltags = TagField(required=False, widget=LabelWidget)
    body=forms.CharField(widget=FroalaEditor)
    class Meta:
        model=Post
        fields=["title","body","image","category","status"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}) ,
            'status':forms.Select(attrs={'class': 'form-control'}),  
            }


# for sharing post 
class EmailPostForm(forms.Form):
    to= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    comments=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))