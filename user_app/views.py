from django.shortcuts import render, redirect, get_object_or_404
from .models import RegularUser, Event, File, VerifiedUser
from .forms import UserForm, LoginForm, CredentialForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import (  UserSerializer, 
                            RegularUserSerializer, 
                            RegularUserGetSerializer,
                            UserDetailSerializer, 
                            RegularUserDetailSerializer, 
                            RegularUserUpdateSerializer, 
                            EventSerializer,
                            RegularUserPaymentSerializer,
                            RegularUserPaymentIdSerializer,
                            RegularUserEventSerializer,
                            FileSerializer,
                            UserVerificationSerializer,
                            FileUploadSerializer,
                        )
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from allauth.account.models import EmailAddress





# Homepage View

def homepage(request):
	return render(request, 'user_app/ca.html', {})

def accountpage(request):
	return render(request, 'user_app/homepage.html', {})

def events(request):
    return render(request, 'user_app/events.html', {})

def index(request):
    return render(request, 'user_app/index.html', {})



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
            regular_user.fb_id=request.data.get('fb_id')
            try:
            	token = Token.objects.get(user = request.user)
            except:
            	token = request.META.get('HTTP_AUTHORIZATION')[7:]
            try:
                suggested_regular_user = RegularUser.objects.get(referral = serializer.validated_data['suggested_referral'])
                if suggested_regular_user:
                    suggested_regular_user.total_points += 10
                    suggested_regular_user.save()
            except:
                pass
            

            regular_user.referral = 'FE' + str(token)[:8]
            regular_user.save()
            if regular_user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    def get(self, request, format = 'json'):
        regular_user = RegularUser.objects.get(user = request.user)
        ranked_regular_users = RegularUser.objects.all().order_by('-total_points')
        for index, value in enumerate(ranked_regular_users):
            if value == regular_user:
                rank = index + 1
        print(rank)
        serializer = RegularUserGetSerializer(regular_user)
        json = {
            'rank' : rank,
        }
        json.update(serializer.data)
        return Response(json, status = status.HTTP_200_OK)

    	

    def put(self, request, format = 'json'):
    	regular_user = RegularUser.objects.get(user = request.user)
    	serializer = RegularUserSerializer(regular_user, data = request.data, partial = True)
    	if serializer.is_valid():
    		print(request.META.get('HTTP_AUTHORIZATION'))
    		serializer.save()
    		return Response(serializer.data, status = status.HTTP_200_OK)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventsApiView(APIView):
    def get(self, request, format = 'json'):
        event = Event.objects.all()
        serializer = EventSerializer(event,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
	
class UserVerificationView(APIView):
    serializer_class = UserVerificationSerializer

    def post(self, request, format='json'):
        new_verified_user = VerifiedUser(user = self.request.user)
        new_verified_user.save()
        json = {
            'status' : 'verified'
        }
        return Response(json, status = status.HTTP_200_OK)
    def get(self, request, format = 'json'):
        verified_user = VerifiedUser.objects.filter(user = self.request.user).count()
        if verified_user:
            json = {
                'status' : 'verified'
            }
        else:
            json = {
                'status' : 'not verified'
            }
        return Response(json, status = status.HTTP_200_OK)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventUpdateAdminViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class RegularUserPaymentView(generics.RetrieveUpdateAPIView):
    serializer_class = RegularUserPaymentSerializer

    def get_object(self):
        user = self.request.user
        return RegularUser.objects.get(user = user)

class RegularUserPaymentIdView(generics.RetrieveUpdateAPIView):
    serializer_class = RegularUserPaymentIdSerializer

    def get_object(self):
        user = self.request.user
        return RegularUser.objects.get(user = user)

class RegularUserEventView(APIView):
    serializer_class = RegularUserEventSerializer

    def get(self, request, format = 'json'):
        regular_user = RegularUser.objects.get(user = request.user)
        event_list = regular_user.event.all()
        regular_user.subsciption_amount = sum([i.points for i in event_list])
        json = {
            'subscription_amount' : regular_user.subsciption_amount
        }
        return Response(json, status = status.HTTP_200_OK)

    def put(self, request, format = 'json'):
        regular_user = RegularUser.objects.get(user = request.user)
        event = Event.objects.get(id = request.data['event_id'])
        check = True if request.data['add_or_remove'] == 'add' else False
        if check:
            regular_user.event.add(event)
            event_list = regular_user.event.all()
            regular_user.subsciption_amount = sum([i.points for i in event_list])
            json = {
                'status' : 'Event Added',
                'subscription_amount' : regular_user.subsciption_amount
            }
            return Response(json, status = status.HTTP_200_OK)
        else:
            regular_user.event.remove(event)
            event_list = regular_user.event.all()
            regular_user.subsciption_amount = sum([i.points for i in event_list])
            json = {
                'status' : 'Event Removed',
                'subscription_amount' : regular_user.subsciption_amount
            }
            return Response(json, status = status.HTTP_200_OK)

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data = request.data)
        if file_serializer.is_valid():
            event = Event.objects.get(id = file_serializer.validated_data['id'])
            print(event)
            file = File.objects.create(user = request.user, event = event, file = file_serializer.validated_data['file'])
            # file = file_serializer.save(user = request.user, event = event)
            file.save()
            return Response(file_serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data = request.data)
        if file_serializer.is_valid():
            event = Event.objects.get(id = file_serializer.validated_data['id'])
            print(event)
            file = File.objects.create(user = request.user, event = event, file = file_serializer.validated_data['file'])
            # file = file_serializer.save(user = request.user, event = event)
            file.save()
            return Response(file_serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class FileGenericView(generics.ListAPIView):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    # queryset = File.objects.all()
    def get_queryset(self):
        return File.objects.filter(user = self.request.user)

class LeaderBoardView(APIView):

    def get(self, request, format = 'json'):
        regular_user = RegularUser.objects.all().order_by('-total_points')
        json = []
        for i in regular_user:
            if(i.user == request.user):
                json += [
                    {
                        'id' : i.pk,
                        'name' : i.name,
                        'points' : i.total_points,
                        'college' : i.college,
                        'current_user' : True,
                    }
                ]
            else:
                json += [
                    {
                        'id' : i.pk,
                        'name' : i.name,
                        'points' : i.total_points,
                        'college' : i.college,
                        'current_user' : False,
                    }
                ]

        return Response(json, status = status.HTTP_200_OK)

class PeersView(APIView):

    def get(self, request, format = 'json'):
        if EmailAddress.objects.filter(user = self.request.user, verified = True).exists():
            json = {
                'status' : 'verified',
            }
        else:
            json = {
                'status' : 'not verified',
            }
        return Response(json, status = status.HTTP_200_OK)

        

        


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


def example_login(request):
    return render(request, 'register/login-page.html', {})









