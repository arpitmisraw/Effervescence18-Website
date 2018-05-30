from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user_detail', views.UserViewSet)
router.register('regular_user_detail', views.RegularUserViewSet)


urlpatterns = [
	path('', views.index, name = 'index'),
	path('register/', views.register, name = 'register'),
	path('login/', views.login_view, name = 'login'),
	path('logout/', views.log_out, name = 'logout'),
	path('credentials/', views.credentials, name = 'credentials'),
	path('create_user/', views.UserCreate.as_view(), name = 'create_user'),
	path('create_regular_user/', views.RegularUserCreate.as_view(), name = 'create_regular_user'),
	path('obtain_auth/', rest_framework_views.obtain_auth_token),
	path('info/', views.ExampleView.as_view(), name = 'info'),
	path('', include(router.urls)),
]