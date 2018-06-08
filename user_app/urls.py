from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views




urlpatterns = [
	path('', views.index, name = 'index'),
	path('register/', views.register, name = 'register'),
	path('login/', views.login_view, name = 'login'),
	path('logout/', views.log_out, name = 'logout'),
	path('credentials/', views.credentials, name = 'credentials'),
	path('create_regular_user/', views.RegularUserCreate.as_view(), name = 'create_regular_user'),
	path('update_regular_user/', views.RegularUserUpdate.as_view(), name = 'update_regular_user'),
	# path('update_regular_user/', views.GetAndUpdateRegularUser.as_view()),
	path('obtain_auth/', rest_framework_views.obtain_auth_token),
	path('user_login/', views.login),
	path('user_logout/', views.logout, name = 'user_logout'),
	path('new_user/', views.new_user, name = 'new_user'),
	path('user_details/', views.user_details),
]