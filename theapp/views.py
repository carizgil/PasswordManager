from django.shortcuts import redirect, render

from theproject import settings
from .forms import LoginForm, NuevoUsuarioForm, NuevaCuentaForm, DetallesCuentaForm, GestionarPerfilForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Cuenta
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import random

#  ------ VISTAS DE LOS CORREOS ELECTRÓNICOS ------ #

def enviar_token_email(user_email, token):
    send_mail(
        subject="Tu token de inicio de sesión",
        message=f"Tu token de inicio de sesión es: {token}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )


# ---- VISTAS DE LA APLICACIÓN ---- #

# Vista para el login

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Autenticar al usuario
            user = authenticate(request, username=email, password=password)

            if user:
                # Generar token aleatorio de 6 dígitos
                token = random.randint(100000, 999999)

                # Guardar en sesión temporal
                request.session['pending_user_id'] = user.id
                request.session['login_token'] = str(token)

                # Mostrar token en la terminal
                print(f"Token temporal para login de {user.email}: {token}")
                
                # Enviar el token por correo electrónico
                # send_mail(
                #     subject="Tu token de inicio de sesión",
                #     message=f"Tu token de inicio de sesión es: {token}",
                #     from_email=settings.DEFAULT_FROM_EMAIL,
                #     recipient_list=[user.email],
                #     fail_silently=False,
                # )

                # Redirigir a la página de verificación de token
                return redirect("verificartoken")
            else:
                return render(request, "login.html", {"form": form, "error": "Credenciales inválidas"})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

# Vista para la verificación del token
def verificar_token_view(request):
    if request.method == "POST":
        token_ingresado = request.POST.get("token")
        token_esperado = request.session.get("login_token")
        user_id = request.session.get("pending_user_id")

        if token_ingresado == token_esperado and user_id:
            user = User.objects.get(id=user_id)
            login(request, user)

            # Limpiar la sesión temporal
            del request.session['pending_user_id']
            del request.session['login_token']

            return redirect("principal")
        else:
            return render(request, "verificartoken.html", {"error": "Token inválido. Inténtalo de nuevo."})
        
    return render(request, "verificartoken.html")

# Vista para el logout    
def logout_view(request):
    logout(request)
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Vista para el registro de nuevos usuarios
def registro_view(request):
    form = NuevoUsuarioForm(request.POST)
    
    if form.is_valid():
        nombre = form.data.get('nombre')
        apellido = form.data.get('apellido')
        email = form.data.get('email')
        password = form.data.get('password')
        confirm_password = form.data.get('confirm_password')
        
        if password != confirm_password:
            error = "Las contraseñas no coinciden."
            return render(request, 'registro.html', {'form': form, 'error': error})
        
        if User.objects.filter(email=email).exists():
            error = "El correo electrónico ya está registrado."
            return render(request, 'registro.html', {'form': form, 'error': error})
        
        User.objects.create_user(
            username=email,
            first_name=nombre,
            last_name=apellido,
            email=email,
            password=password
        )
        
        # Autenticar y loguear al usuario automaticamente
        user = authenticate(request, username=email, password=password)
        login(request, user)
        
        return redirect('principal')
    else:
        form = NuevoUsuarioForm()
        return render(request, 'registro.html', {'form': form})
    
# Vista principal que muestra las cuentas del usuario
def principal_view(request):
    orden = request.GET.get('orden', 'antiguos')
    busqueda = request.GET.get('busqueda', '')

    cuentas = Cuenta.objects.filter(usuario=request.user)

    if busqueda:
        cuentas = cuentas.filter(
            nombre_cuenta__icontains=busqueda
        ) | cuentas.filter(
            username__icontains=busqueda
        )

    if orden == 'az':
        cuentas = cuentas.order_by('nombre_cuenta')
    elif orden == 'za':
        cuentas = cuentas.order_by('-nombre_cuenta')
    elif orden == 'recientes':
        cuentas = cuentas.order_by('-id')
    elif orden == 'antiguos':
        cuentas = cuentas.order_by('id')

    paginator = Paginator(cuentas, 6)  # 6 cuentas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'principal.html', {
        'cuentas': page_obj,
        'orden': orden,
        'busqueda': busqueda
    })


# Vista para agregar una nueva cuenta
def nuevacuenta_view(request):
    if request.method == 'POST':
        form = NuevaCuentaForm(request.POST, request.FILES)
        if form.is_valid():
            Cuenta.objects.create(
                usuario=request.user,
                nombre_cuenta=form.cleaned_data['nombre_cuenta'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                url=form.cleaned_data['url'],
                notas=form.cleaned_data['notas'],
                icon=form.cleaned_data['icon']
            )
            return redirect('principal')
    else:
        form = NuevaCuentaForm()

    return render(request, 'nuevacuenta.html', {'form': form})

# Vista para eliminar una cuenta
def eliminarcuenta_view(request, cuenta_id):
    cuenta = Cuenta.objects.get(id=cuenta_id, usuario=request.user)
    cuenta.delete()
    return redirect('principal')

def detallescuenta_view(request, cuenta_id):
    cuenta = Cuenta.objects.get(id=cuenta_id, usuario=request.user)

    if request.method == 'POST':
        form = DetallesCuentaForm(request.POST, request.FILES)
        if form.is_valid():
            cuenta.nombre_cuenta = form.cleaned_data['nombre_cuenta']
            cuenta.username = form.cleaned_data['username']
            cuenta.url = form.cleaned_data['url']
            cuenta.notas = form.cleaned_data['notas']
            cuenta.password = form.cleaned_data['password']

            icon_data = form.cleaned_data.get('icon')

            # Comprobar si el usuario quiere eliminar el icono existente
            if isinstance(icon_data, bool) and icon_data is False:
                # El usuario marcó "Clear"
                if cuenta.icon:
                    cuenta.icon.delete(save=False)
                cuenta.icon = None
            elif icon_data:
                # Subió un archivo nuevo
                cuenta.icon = icon_data
            # Si icon_data es None y no se marcó Clear, dejamos el icono actual

            cuenta.save()
            msg = "Cuenta actualizada correctamente."
            return render(request, 'detallescuenta.html', {'form': form, 'cuenta': cuenta, 'msg': msg})
    else:
        form = DetallesCuentaForm(initial={
            'nombre_cuenta': cuenta.nombre_cuenta,
            'username': cuenta.username,
            'url': cuenta.url,
            'notas': cuenta.notas,
            'icon': cuenta.icon,
            'password': cuenta.password
        })

    return render(request, 'detallescuenta.html', {'form': form, 'cuenta': cuenta})

# Vista para eliminar la cuenta del usuario
def eliminarusuario_view(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('login')

def detallesperfil_view(request):
    user = request.user

    if request.method == 'POST':
        form = GestionarPerfilForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellido']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['email']

            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Si escribió una nueva contraseña
            if password or confirm_password:
                if password != confirm_password:
                    error = "Las contraseñas no coinciden."
                    return render(request, 'detallesperfil.html', {'form': form, 'error': error})
                else:
                    user.set_password(password)
                    update_session_auth_hash(request, user)  # Mantener la sesión activa después de cambiar la contraseña
                    

            user.save()
            msg = "Perfil actualizado correctamente."

            return render(request, 'detallesperfil.html', {'form': form, 'msg': msg})

    else:
        form = GestionarPerfilForm(initial={
            'nombre': user.first_name,
            'apellido': user.last_name,
            'email': user.email
        })

    return render(request, 'detallesperfil.html', {'form': form})

