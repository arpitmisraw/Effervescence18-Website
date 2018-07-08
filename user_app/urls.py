from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events', views.EventViewSet, base_name = 'event')
router.register('events_update', views.EventUpdateAdminViewSet, base_name = 'event_update')



urlpatterns = [

	# homepage
	path('', views.homepage, name = 'homepage'),



	# url for API for user details
	path('api/regular_user/', views.RegularUserAPI.as_view(), name = 'regular_user'),

	# urls for forms
	path('user_login/', views.login, name = 'user_login'),
	path('user_logout/', views.logout, name = 'user_logout'),
	path('set_new_user/', views.new_user, name = 'new_user'),
	path('set_user_details/', views.user_details, name = 'set_user_details'),
	path('change_user_details/', views.change_user_details, name = 'change_user_details'),
	path('', include(router.urls)),
	re_path(r'^event_details/(?P<pk>[0-9]+)$', views.EventView.as_view()),
	path('user_detail/', views.UserAPIView.as_view()),
]