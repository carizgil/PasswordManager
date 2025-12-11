from django.contrib import admin

from .models import Cuenta

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cuenta', 'username', 'usuario')
    search_fields = ('nombre_cuenta', 'username', 'usuario__email')
