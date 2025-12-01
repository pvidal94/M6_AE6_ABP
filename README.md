📦 Plataforma de Gestión de Productos: Control de Acceso (RBAC) con Django

Este repositorio contiene una solución Full-Stack Backend que implementa un sistema de gestión de inventario construido sobre el framework Django. Su principal característica es un Control de Acceso Basado en Roles (RBAC) granular y totalmente personalizado para administrar productos desde el panel administrativo.

El objetivo es proporcionar un proyecto base listo para expandirse, con permisos, roles y datos iniciales configurados automáticamente.

✨ Características Principales

Acceso Granular: Tres niveles de acceso predefinidos (Administrador, Gestor, Solo Lectura).

Restricción por Grupo: La lógica de acceso está centralizada en inventario/admin.py, lo que limita acciones como eliminar según el rol del usuario.

Restricción por Campo: El rol Gestor solo puede editar campos críticos (price, stock); el resto se vuelve de solo lectura.

Inicialización Automática: Script que crea usuarios de prueba, grupos, permisos y productos iniciales al inicio.

⚠️ Licencia y Uso Libre

Este proyecto está bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente para fines personales o comerciales.
¡Contribuciones y mejoras son bienvenidas!

🚀 Guía de Configuración Rápida (Deploy Inmediato)

Sigue estos pasos desde tu terminal (PowerShell o Bash), con tu entorno virtual activado si corresponde.

1. Clonar, Instalar y Migrar
# Clonar el repositorio
git clone https://github.com/pvidal94/M6_AE6_ABP.git
cd M6_AE6_ABP

# Activar entorno virtual (ejemplo Windows)
.\venv\Scripts\Activate.ps1

# Instalar dependencias (solo Django)
pip install django

# Aplicar migraciones
python manage.py makemigrations inventario
python manage.py migrate

2. Crear Superusuario (Maestro)

Este usuario administra completamente el proyecto.

python manage.py createsuperuser
# Usuario recomendado: maestro
# Contraseña: TU_CONTRASEÑA_SEGURA

3. Configuración Automática de Roles y Datos

Ejecuta el shell de Django:

python manage.py shell


Ahora pega el siguiente script completo:

from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from inventario.models import Product
from decimal import Decimal

# --- 1. DEFINICIÓN DE PERMISOS Y GRUPOS ---
print("1. Definiendo permisos, grupos y roles...")

ct = ContentType.objects.get_for_model(Product)
p_add = Permission.objects.get(codename='add_product', content_type=ct)
p_change = Permission.objects.get(codename='change_product', content_type=ct)
p_delete = Permission.objects.get(codename='delete_product', content_type=ct)
p_view = Permission.objects.get(codename='view_product', content_type=ct)
p_view_only, _ = Permission.objects.get_or_create(
    codename='can_view_only',
    name='Solo puede ver productos',
    content_type=ct
)

admin_group, _ = Group.objects.get_or_create(name='Administradores')
manager_group, _ = Group.objects.get_or_create(name='Gestores_de_Productos')

admin_group.permissions.set([p_add, p_change, p_delete, p_view])
manager_group.permissions.set([p_add, p_change, p_view])

# --- 2. CREACIÓN DE USUARIOS DE PRUEBA ---
print("2. Creando usuarios de prueba (password: 1234)...")

admin_user, created = User.objects.get_or_create(
    username='admin_gestor',
    defaults={'is_staff': True, 'email': 'admin@demo.com'}
)
if created:
    admin_user.set_password('1234')
admin_user.groups.add(admin_group)
admin_user.save()

manager_user, created = User.objects.get_or_create(
    username='manager_user',
    defaults={'is_staff': True, 'email': 'manager@demo.com'}
)
if created:
    manager_user.set_password('1234')
manager_user.groups.add(manager_group)
manager_user.save()

viewer_user, created = User.objects.get_or_create(
    username='viewer_only',
    defaults={'is_staff': True, 'email': 'viewer@demo.com'}
)
if created:
    viewer_user.set_password('1234')
viewer_user.user_permissions.add(p_view_only)
viewer_user.save()

# --- 3. CARGA DE PRODUCTOS INICIALES ---
print("3. Cargando datos iniciales de producto...")

productos_iniciales = [
    {"name": "Laptop Ejecutiva Modelo X900", "description": "Estación de trabajo potente.", "price": Decimal("1299.99"), "stock": 15},
    {"name": "Monitor Curvo 4K UltraWide", "description": "34 pulgadas, 144Hz para gaming.", "price": Decimal("499.50"), "stock": 35},
    {"name": "Teclado Mecánico RGB Pro", "description": "Switches táctiles, chasis aluminio.", "price": Decimal("75.00"), "stock": 80},
    {"name": "Mouse Inalámbrico Ergonómico", "description": "Diseño vertical recargable.", "price": Decimal("25.99"), "stock": 120},
    {"name": "Webcam HD 1080p con Micrófono", "description": "Autoenfoque ideal para videollamadas.", "price": Decimal("45.25"), "stock": 50},
]

for data in productos_iniciales:
    Product.objects.get_or_create(name=data['name'], defaults=data)

print("\n🎉 CONFIGURACIÓN COMPLETADA.")


Salir del shell:

exit()

4. Iniciar Servidor y Acceder
python manage.py runserver
