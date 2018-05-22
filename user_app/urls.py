from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('', views.index, name = 'index'),
	path('register/', views.UserFormView.as_view(), name = 'register'),
	path('login/', views.login_view, name = 'login'),
	path('logout/', views.log_out, name = 'logout'),
]