from django.shortcuts import render, redirect
from .models import RegularUser
from .forms import UserForm, LoginForm, CredentialForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegularUserSerializer, LoginSerializer, UserDetailSerializer, RegularUserDetailSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from rest_framework import viewsets




# NORMAL VIEWS

def log_out(request):
	logout(request)
	return redirect('login')

def login_view(request):
	print(request.user)
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
	if request.user.is_authenticated:
		current_user = RegularUser.objects.filter(user = request.user)
		print(current_user)
		context = {'current_user' : current_user, 'name' : current_user[0].name}
		return render(request, 'user_app/index.html', context)
	else:
		return redirect('login')


def credentials(request):
	if request.user.is_anonymous:
		return redirect('register')
	elif RegularUser.objects.filter(user = request.user).exists():
		regular_user = RegularUser.objects.filter(user = request.user).first()
		form = CredentialForm(instance = regular_user)
		return render(request, 'user_app/credentials.html', {'form' : form})
	else:
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
			token = Token.objects.create(user=user)
			user = authenticate(username = username, password = password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('credentials')
		return render(request, 'user_app/registration_form.html', {'form' : form})
	else:
		form = UserForm()
		return render(request, 'user_app/registration_form.html', {'form' : form})



# API VIEWS



class RegularUserCreate(APIView):
    serializer_class = RegularUserSerializer

    def post(self, request, format='json'):
        serializer = RegularUserSerializer(data=request.data)
        if serializer.is_valid():
            regular_user = serializer.save()
            regular_user.user = request.user
            token = Token.objects.get(user = request.user)
            regular_user.referral = 'FE' + str(token)[:8]
            regular_user.save()
            if regular_user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format = None):
    	regular_user = RegularUser.objects.get(user = request.user)
    	json = {
    		'name' : regular_user.name,
    		'college' : regular_user.college,
    		'check' : regular_user.check,
    		'birthday' : regular_user.birthday,
    		'gender' : regular_user.gender,
    		'phone' : regular_user.phone,
    		'referral' : regular_user.referral,
    	}
    	return Response(json)


class GetAndUpdateRegularUser(generics.RetrieveUpdateAPIView):
	queryset = RegularUser.objects.all()
	serializer_class = RegularUserSerializer
	lookup_field = 'name'



def login(request):
	return render(request, 'register/user_login.html', {})

def user_details(request):
	return render(request, 'register/user_details.html', {})







