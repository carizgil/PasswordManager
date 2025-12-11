# SecurePass - Proyecto Django
SecurePass es una página web de gestión de contraseñas que permite a los usuarios almacenar y gestionar sus contraseñas de manera segura. Incluye registro de usuarios, autenticación y verificación por token.

# Tecnologías utilizadas
- Python 
- Django
- SQLite
- Pillow
- GitHub Codespaces con devcontainer.json para configuración automática del entorno

# Ejecución en GitHub Codespaces

1. Abrir el repositorio en GitHub.
2. Hacer clic en Code --> Create Codespace on main.
3. Esperar a que se inicialice el entorno (GitHub instalará las dependencias desde requirements.txt).
4. Cuando el Codespaces esté listo, ejecutar las migraciones:
    python manage.py migrate
5. Iniciar el servidor:
    python manage.py runserver 0.0.0.0:8000
6. GitHub abrirá automáticamente la URL donde corre la aplicación.
7. Crear un usuario y comenzar a usar la página web.

# Estructura del proyecto
PasswordManager/
├─ manage.py
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ .devcontainer/
|    ├─  devcontainer.json
├─  theapp/
|    ├─ __init__.py
|    ├─ admin.py
|    ├─ apps.py
|    ├─ forms.py
|    ├─ models.py
|    ├─ tests.py
|    ├─ urls.py
|    ├─ views.py
|    ├─ migrations/
|    ├─ statics/
|    |    ├─ css/
|    |    |    ├─ estilo_detallescuenta.css
|    |    |    ├─ estilo_login.css
|    |    |    ├─ estilo_nuevacuenta.css
|    |    |    ├─ estilo_principal.css
|    |    |    ├─ estilo_recuperacion.css
|    |    |    ├─ estilo_registro.css
|    |    |    └─ estilo_token.css
|    |    ├─ images/
|    |    |     └─ favicon.ico
|    └─ templates/
|        ├─ recuperar/
|        |    ├─ base_recuperacion.html
|        |    ├─ password_reset_complete.html
|        |    ├─ password_reset_confirm.html
|        |    ├─ password_reset_done.html
|        |    └─ password_reset_form.html
|        ├─ detallescuenta.html
|        ├─ detallesperfil.html
|        ├─ login.html
|        ├─ nuevacuenta.html
|        ├─ olvidopass.html
|        ├─ principal.html
|        ├─ registro.html
|            └─ verificartoken.html
└─theproject/
    ├─ __init__.py
    ├─ asgi.py
    ├─ settings.py
    ├─ urls.py
    └─ wsgi.py

# Uso básico

## Registro/Login
- Crear un usuario o iniciar sesión.
- Verificación por token de 6 dígitos en la terminal.

## Añadir cuentas
- Completar el formulario con:
  - Nombre de la cuenta (Obligatorio)
  - Username (Obligatorio)
  - Password (Obligatorio)
  - URL (Opcional)
  - Notas (Opcional)
  - Icono (Opcional)

## Editar/Eliminar cuentas
- Botón azul: ver o editar información de la cuenta.
- Botón rojo: eliminar cuenta.

## Buscar y filtrar
- Buscar cuentas por nombre.
- Filtrar por:
  - Nombre A → Z o Z → A
  - Recientes primero o últimos primero

## Recuperar contraseña
- Hacer clic en “Olvidé mi contraseña”.
- Ingresar el correo registrado.
- Recibir un token de verificación (en desarrollo, se muestra en la terminal).
- Restablecer la contraseña y volver a iniciar sesión.

## Configuración de usuario
- Editar información personal (nombre, apellidos, contraseña, correo).
- Darse de baja de la plataforma.