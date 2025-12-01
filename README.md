Plataforma de Gestión de Productos: Despliegue Rápido

Este repositorio contiene la implementación de una plataforma administrativa de inventario en Django, destacando un sistema de control de acceso (RBAC) avanzado para gestionar productos con diferentes niveles de privilegio.

El objetivo es tener un sistema completamente configurado con roles de Administrador, Gestor de Productos y Solo Lectura en menos de 5 minutos.

🚀 Guía de Configuración

Sigue estos 5 pasos en tu terminal (PowerShell, con el entorno virtual (venv) activo).

1. Clonar, Instalar y Migrar

Asegúrate de estar en el directorio raíz del proyecto (M6_AE6_ABP).

# Instalar dependencias (solo Django)
pip install django

# Aplicar migraciones iniciales y de la aplicación 'inventario'
python manage.py makemigrations inventario
python manage manage.py migrate


2. Crear Superusuario (Maestro)

Este usuario tendrá acceso total a la configuración y gestión del sistema.

python manage.py createsuperuser
# Usar: Usuario: maestro | Contraseña: tu_contraseña_secreta


3. Configuración Automática de Roles y Datos

Abre el Django Shell e inmediatamente copia y pega el siguiente script completo. Este script crea los grupos, los usuarios de prueba y los productos iniciales, asignando todos los permisos de forma automática.

python manage.py shell


Copia y pega este bloque completo en el shell:

from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from inventario.models import Product
from decimal import Decimal

# --- 1. DEFINICIÓN DE PERMISOS ---
print("1. Definiendo permisos y grupos...")

# Obtener ContentType para el modelo Producto
ct = ContentType.objects.get_for_model(Product)

# Obtener permisos básicos de Django para Producto
p_add = Permission.objects.get(codename='add_product', content_type=ct)
p_change = Permission.objects.get(codename='change_product', content_type=ct)
p_delete = Permission.objects.get(codename='delete_product', content_type=ct)
p_view = Permission.objects.get(codename='view_product', content_type=ct)

# Obtener permiso personalizado 'Can view only'
p_view_only, _ = Permission.objects.get_or_create(
    codename='can_view_only', 
    name='Solo puede ver productos', 
    content_type=ct
)

# --- 2. CREACIÓN DE GRUPOS ---
admin_group, _ = Group.objects.get_or_create(name='Administradores')
manager_group, _ = Group.objects.get_or_create(name='Gestores_de_Productos')

# Asignación de permisos a Administradores (Total Control)
admin_group.permissions.set([p_add, p_change, p_delete, p_view])

# Asignación de permisos a Gestores (No puede Eliminar)
manager_group.permissions.set([p_add, p_change, p_view])

# --- 3. CREACIÓN DE USUARIOS DE PRUEBA ---
print("2. Creando usuarios de prueba...")

# Usuario 1: admin_gestor (Administrador)
admin_user, created = User.objects.get_or_create(username='admin_gestor', defaults={'is_staff': True, 'email': 'admin@demo.com'})
if created: admin_user.set_password('1234') # Contraseña fácil para demo
admin_user.groups.add(admin_group)
admin_user.save()
print(f"Usuario {admin_user.username}: Creado y asignado a Administradores.")

# Usuario 2: manager_user (Gestor de Productos)
manager_user, created = User.objects.get_or_create(username='manager_user', defaults={'is_staff': True, 'email': 'manager@demo.com'})
if created: manager_user.set_password('1234')
manager_user.groups.add(manager_group)
manager_user.save()
print(f"Usuario {manager_user.username}: Creado y asignado a Gestores de Productos.")

# Usuario 3: viewer_only (Solo Lectura)
viewer_user, created = User.objects.get_or_create(username='viewer_only', defaults={'is_staff': True, 'email': 'viewer@demo.com'})
if created: viewer_user.set_password('1234')
viewer_user.user_permissions.add(p_view_only)
viewer_user.save()
print(f"Usuario {viewer_user.username}: Creado con permiso Solo Lectura.")

# --- 4. CARGA DE PRODUCTOS INICIALES (Datos de Muestra) ---
print("3. Cargando datos iniciales de producto...")

productos_iniciales = [
    {"name": "Laptop Ejecutiva Modelo X900", "description": "Estación de trabajo potente.", "price": Decimal("1299.99"), "stock": 15},
    {"name": "Monitor Curvo 4K UltraWide", "description": "34 pulgadas, 144Hz para gaming.", "price": Decimal("499.50"), "stock": 35},
    {"name": "Teclado Mecánico RGB Pro", "description": "Switches táctiles y chasis de aluminio.", "price": Decimal("75.00"), "stock": 80},
    {"name": "Mouse Inalámbrico Ergonómico", "description": "Diseño vertical, batería recargable.", "price": Decimal("25.99"), "stock": 120},
    {"name": "Webcam HD 1080p con Micrófono", "description": "Video conferencias con autoenfoque.", "price": Decimal("45.25"), "stock": 50},
]

for data in productos_iniciales:
    Product.objects.get_or_create(name=data['name'], defaults=data)

print("\n🎉 CONFIGURACIÓN COMPLETADA.")


Una vez que el script finalice, sal del shell:

exit()


4. Iniciar Servidor y Pruebas

python manage.py runserver


Accede a http://127.0.0.1:8000/admin/.

Usuario Patricia_Vidal

Contraseña TheStrokes94.

Rol y Prueba

admin_gestor

TheStrokes94.

Administrador: Puede añadir, editar y eliminar productos.

manager_user

TheStrokes94.

Gestor: Puede añadir y editar, pero NO puede eliminar. Campos Nombre/Descripción son solo lectura.

viewer_only

TheStrokes94.

Solo Lectura: Solo ve el listado, no puede editar ni crear.
