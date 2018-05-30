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

class UserCreate(APIView):
    serializer_class = UserSerializer

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key

                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegularUserCreate(APIView):
    serializer_class = RegularUserSerializer

    def post(self, request, format='json'):
        serializer = RegularUserSerializer(data=request.data)
        if serializer.is_valid():
            regular_user = serializer.save()
            regular_user.user = request.user
            regular_user.save()
            if regular_user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def UserLogin(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
			if user.is_active:
				token, created = Token.objects.get_or_create(user=user)
				request.session['auth'] = token.key
				return redirect('/', request)
	return redirect(settings.LOGIN_URL, request)





class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': str(request.user), 
            'auth': str(request.auth),  
        }
        return Response(content)   

class UserDetail(generics.RetrieveDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer
	lookup_field = 'username'


class RegularUserViewSet(viewsets.ModelViewSet):
	queryset = RegularUser.objects.all()
	serializer_class = RegularUserDetailSerializer
	lookup_field = 'name'