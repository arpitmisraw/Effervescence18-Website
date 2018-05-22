from django.views import generic
from django.shortcuts import render, redirect
from .models import RegularUser
from .forms import UserForm, LoginForm, CredentialForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def log_out(request):
	logout(request)
	return redirect('login')

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		user = User(username = request.POST['username'], password = request.POST['password'])
		user = authenticate(username = user.username, password = user.password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('index')
		else:
			print("Too bad")
			form = LoginForm()
			context = {'form' : form}
			return render(request, 'user_app/login_form.html', context)


			

	else:
		form = LoginForm()
	context = {'form' : form}
	return render(request, 'user_app/login_form.html', context)










def index(request):
	print(request.user)
	current_user = RegularUser.objects.filter(user = request.user)
	context = {'current_user' : current_user, 'name' : current_user[0].name}
	return render(request, 'user_app/index.html', context)


def credentials(request):
	print(request.user)
	if request.method == 'POST':
		form = CredentialForm(request.POST)

		if form.is_valid():
			regular_user = form.save(commit = False)
			regular_user.user = request.user
			regular_user.save()
			return redirect('index')
		return render(request, 'user_app/index.html', {'form' : form})
	else:
		form = CredentialForm()
		return render(request, 'user_app/credentials.html', {'form' : form})


def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)

		if form.is_valid():
			user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			user = authenticate(username = username, password = password)

			if user is not None:
				if user.is_active:
					login(request, user)
					print('Done!')
					print(request.user)
					return redirect('credentials')
		return render(request, 'user_app/registration_form.html', {'form' : form})
	else:
		form = UserForm()
		return render(request, 'user_app/registration_form.html', {'form' : form})









