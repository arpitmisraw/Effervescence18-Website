from django import forms
from .models import RegularUser
from django.contrib.auth.models import User





class LoginForm(forms.ModelForm):	
	class Meta:
		
		model = User
		fields = ['username', 'password']

		widgets = {
			'username' : forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'Enter Username'}),
			'password' : forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder' : 'Enter Password'}),
		}

	
class UserForm(forms.ModelForm):	
	class Meta:
		
		model = User
		fields = ['username', 'email', 'password']

		widgets = {
			'username' : forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'Enter Username'}),
			'password' : forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder' : 'Enter Password'}),
			'email' : forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'Enter Email'}),

		}

class CredentialForm(forms.ModelForm):
	class Meta:
		model = RegularUser
		fields = ['name', 'college', 'birthday', 'gender']






