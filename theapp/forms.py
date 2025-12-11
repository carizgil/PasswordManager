from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
class NuevoUsuarioForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
class GestionarPerfilForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    email = forms.EmailField(label="Email")

    password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(),
        required=False
    )

    confirm_password = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(),
        required=False
    )

    
class NuevaCuentaForm(forms.Form):
    nombre_cuenta = forms.CharField(label="Nombre de la Cuenta", max_length=100)
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    url = forms.URLField(label="URL", required=False)
    notas = forms.CharField(label="Notas", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    icon = forms.ImageField(label="Icono de la Cuenta", required=False)
    
class DetallesCuentaForm(forms.Form):
    nombre_cuenta = forms.CharField(label="Nombre de la Cuenta", max_length=100)
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True),  # esto permite que el campo mantenga el valor actual
        required=False
    )
    url = forms.URLField(label="URL", required=False)
    notas = forms.CharField(label="Notas", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    icon = forms.ImageField(label="Icono de la Cuenta", required=False)
    
# class DetallesCuentaForm(forms.Form):
#     nombre_cuenta = forms.CharField(label="Nombre de la Cuenta", max_length=100)
#     username = forms.CharField(label="Username", max_length=100)
#     password = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(render_value=True),  # esto permite que el campo mantenga el valor actual
#         required=False
#     )
#     url = forms.URLField(label="URL", required=False)
#     notas = forms.CharField(
#         label="Notas", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False
#     )
#     icon = forms.ImageField(label="Icono de la Cuenta", required=False)