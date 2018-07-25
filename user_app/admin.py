from django.contrib import admin
from .models import RegularUser, Event, File

admin.site.register(RegularUser)
admin.site.register(Event)
admin.site.register(File)

