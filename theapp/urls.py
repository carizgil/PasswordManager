from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('principal/', views.principal_view, name='principal'),
    path('logout/', views.logout_view, name='logout'),
    path('nuevacuenta/', views.nuevacuenta_view, name='nuevacuenta'),
    path('eliminarcuenta/<int:cuenta_id>/', views.eliminarcuenta_view, name='eliminarcuenta'),
    path('detallescuenta/<int:cuenta_id>/', views.detallescuenta_view, name='detallescuenta'),
    path('eliminarcuenta', views.eliminarcuenta_view, name='eliminarcuenta'),
    path('detallesperfil', views.detallesperfil_view, name='detallesperfil'),
    path('verificartoken/', views.verificar_token_view, name='verificartoken'),
]

# Flujo de recuperación de contraseña usando vistas genéricas de Django
urlpatterns += [
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='recuperar/password_reset_form.html'), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='recuperar/password_reset_done.html'),
            name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='recuperar/password_reset_confirm.html', 
            success_url=reverse_lazy('password_reset_complete') ),
            name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='recuperar/password_reset_complete.html'),
            name='password_reset_complete'),
]