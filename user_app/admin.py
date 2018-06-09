from django.contrib import admin
from .models import RegularUser, Event

admin.site.register(RegularUser)
admin.site.register(Event)
