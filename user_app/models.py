from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class RegularUser(models.Model):
	gender_options = (
			('M', 'Male'),
			('F', 'Female'),
			('O', 'Other'),
		)
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
	name = models.CharField(max_length = 40)
	college = models.TextField()
	check = models.BooleanField(default = False)
	birthday = models.DateField(default = timezone.now)
	gender = models.CharField(max_length = 1, choices = gender_options, null = True)
	phone = models.CharField(max_length = 10, null = True)



	def __str__(self):
		return self.name

