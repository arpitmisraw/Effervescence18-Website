from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Event(models.Model):
	event_name = models.CharField(max_length = 100)
	prize = models.IntegerField(null = True)
	description = models.TextField()
	points = models.IntegerField(null = True)
	fee = models.IntegerField(null = True)
	subscription = models.BooleanField(default = False)

	def __str__(self):
		return self.event_name

class RegularUser(models.Model):
	gender_options = (
			('M', 'Male'),
			('F', 'Female'),
			('O', 'Other'),
		)
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
	name = models.CharField(max_length = 40)
	college = models.TextField()
	birthday = models.DateField(default = timezone.now, null = True)
	gender = models.CharField(max_length = 1, choices = gender_options, null = True)
	phone = models.CharField(max_length = 10, null = True)
	referral = models.CharField(max_length = 10, null = True)
	subscription_amount = models.IntegerField(default = 0)
	payment_status = models.BooleanField(default = False)
	payment_id = models.CharField(max_length = 50, null = True, blank=True)
	event = models.ManyToManyField(Event, blank=True)
	total_points = models.IntegerField(blank = True, null = True, default = 0)


	def __str__(self):
		return self.name

class VerifiedUser(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
	verified = models.BooleanField(default = False)

	def __str__(self):
		return self.user.username

class File(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	file = models.FileField(blank = True, null = True)
	# details = models.CharField(max_length = 200, blank = True, null = True)

	def __str__(self):
		return self.user.username