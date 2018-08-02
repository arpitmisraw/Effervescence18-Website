from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import RegularUser, Event, File, VerifiedUser
from django.contrib.auth import authenticate, login, logout




class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=6, max_length=100,
            write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        user = authenticate(username = validated_data['username'], password = validated_data['password'])
        return user


class RegularUserSerializer(serializers.ModelSerializer): 
    phone = serializers.RegexField(regex = r'^[0-9]{10}$')

    class Meta:
        model = RegularUser
        exclude = ['user', 'referral']

    def create(self, validated_data):
        regular_user = RegularUser(
            name = validated_data["name"],
            college = validated_data["college"],
            birthday = validated_data["birthday"],
            gender = validated_data["gender"],
            phone = validated_data["phone"],
            suggested_referral = validated_data["suggested_referral"],
        )
        regular_user.save()
        return regular_user


class RegularUserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = ['subscription_amount']

class RegularUserPaymentIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = ['payment_id']

class RegularUserEventSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    add_or_remove = serializers.CharField(max_length = 20)

class RegularUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        exclude = ['user', 'referral']
    


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegularUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        exclude = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']

    

class FileUploadSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(max_length = 100)
    class Meta:
        model = File
        fields = ['file', 'event_name']



class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedUser
        fields = ['user']
    









