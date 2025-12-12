"""
URL configuration for theproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),
    path('', include('theapp.urls')),
]

# Flujo de recuperación de contraseña usando vistas genéricas de Django
urlpatterns += [
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='recuperar/password_reset_form.html',
            extra_email_context={
                'domain': settings.PASSWORD_RESET_DOMAIN,
                'protocol': settings.PASSWORD_RESET_PROTOCOL,
            }
        ),
        name='password_reset'
    ),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='recuperar/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='recuperar/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='recuperar/password_reset_complete.html'),
         name='password_reset_complete'),
]

# Sirve para archivos multimedia en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
