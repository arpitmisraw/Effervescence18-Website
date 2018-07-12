from django.shortcuts import render, redirect, get_object_or_404
from .models import RegularUser, Event
from .forms import UserForm, LoginForm, CredentialForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegularUserSerializer, UserDetailSerializer, RegularUserDetailSerializer, RegularUserUpdateSerializer, EventSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination





# Homepage View

def homepage(request):
	return render(request, 'user_app/homepage.html', {})

def events(request):
    return render(request, 'user_app/events.html', {})



# API VIEWS


class UserAPIView(APIView):
	serializer_class = UserDetailSerializer

	def get(self, request, format = 'json'):
		username = request.user.username
		json = {
			'username' : username
		}
		return Response(json)

class RegularUserAPI(APIView):
    serializer_class = RegularUserSerializer

    def post(self, request, format='json'):
        serializer = RegularUserSerializer(data=request.data)
        if serializer.is_valid():
            regular_user = serializer.save()
            regular_user.user = request.user
            try:
            	token = Token.objects.get(user = request.user)
            except:
            	token = request.META.get('HTTP_AUTHORIZATION')[7:]
            # print(request.META)	
            regular_user.referral = 'FE' + str(token)[:8]
            regular_user.save()
            if regular_user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    def get(self, request, format = 'json'):
        regular_user = RegularUser.objects.get(user = request.user)
        serializer = RegularUserSerializer(regular_user)
        return Response(serializer.data, status = status.HTTP_200_OK)

    	

    def put(self, request, format = 'json'):
    	regular_user = RegularUser.objects.get(user = request.user)
    	serializer = RegularUserSerializer(regular_user, data = request.data, partial = True)
    	if serializer.is_valid():
    		print(request.META.get('HTTP_AUTHORIZATION'))
    		serializer.save()
    		return Response(serializer.data, status = status.HTTP_200_OK)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventViewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    pagination_class = EventViewPagination

class EventUpdateAdminViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()



# Form Views

def login(request):
	return render(request, 'register/user_login.html', {})


def logout(request):
	return render(request, 'register/user_logout.html', {})


def new_user(request):
	return render(request, 'register/new_user.html', {})
	

def user_details(request):
	return render(request, 'register/user_details.html', {})

def change_user_details(request):
	return render(request, 'register/change_user_details.html', {})

def change_password(request):
    return render(request, 'register/change_password.html', {})







