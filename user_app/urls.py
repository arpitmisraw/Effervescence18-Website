from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views




urlpatterns = [

	# homepage
	path('', views.index, name = 'index'),

	# url for API for user details
	path('api/regular_user/', views.RegularUserAPI.as_view(), name = 'regular_user'),

	# urls for forms
	path('user_login/', views.login, name = 'user_login'),
	path('user_logout/', views.logout, name = 'user_logout'),
	path('set_new_user/', views.new_user, name = 'new_user'),
	path('set_user_details/', views.user_details, name = 'set_user_details'),
	path('change_user_details/', views.change_user_details, name = 'change_user_details'),

	path('user_detail/', views.UserAPIView.as_view()),
]