from django.views import generic
from django.shortcuts import render, redirect
from .models import RegularUser
from .forms import UserForm, LoginForm
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
	current_user = RegularUser.objects.filter(user = request.user)
	context = {'current_user' : current_user, 'name' : current_user[0].name}
	return render(request, 'user_app/index.html', context)












class UserFormView(View):
	form_class = UserForm
	template_name = 'user_app/registration_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form' : form})

	def post(self, request):
		form = self.form_class(request.POST)


		if form.is_valid():
			user = form.save(commit = False)

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			reg_user = RegularUser(user = username)
			reg_user.save()

			user = authenticate(username = username, password = password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('index')

		return render(request, self.template_name, {'form' : form})

