from django.db import models

from django.contrib.auth.models import User

# Modelo para almacenar cuentas 
class Cuenta(models.Model):
    # Un usuario puede tener múltiples cuentas
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_cuenta = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='account_icons/', blank=True, null=True)
    
    