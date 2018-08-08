"""effe_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from allauth.account.views import ConfirmEmailView
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^', include('django.contrib.auth.urls')),
    path('', include('user_app.urls'), name = 'home'),
    path('ca/', TemplateView.as_view(template_name = 'index.html')),
    path('api/', include('rest_auth.urls')),
    path('api/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r'^api/registration/account-confirm-email/(?P<key>\w+)/$', ConfirmEmailView),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)