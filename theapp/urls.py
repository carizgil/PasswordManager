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
    path('eliminarusuario', views.eliminarusuario_view, name='eliminarusuario'),
    path('detallesperfil', views.detallesperfil_view, name='detallesperfil'),
    path('verificartoken/', views.verificar_token_view, name='verificartoken'),
]