PASO 1: INSTALACIÓN Y PREPARACIÓN DE LA BASE DE DATOS

Instalar Django:
pip install django

Ejecutar Migraciones (Crear tablas del sistema y del modelo Producto):
python manage.py makemigrations inventario
python manage.py migrate

Crear el Superusuario (Usuario MAESTRO de configuración):
python manage.py createsuperuser

Usar: Usuario: maestro (o el que desee) | Contraseña: TU_CONTRASEÑA

PASO 2: CONFIGURACIÓN AUTOMÁTICA DE ROLES Y DATOS

Este paso crea los GRUPOS (Administradores, Gestores), los USUARIOS DE PRUEBA y carga los PRODUCTOS INICIALES.

Abrir la consola interactiva de Django (Django Shell):
python manage.py shell

COPIAR Y PEGAR el script completo de configuración (se encuentra en el archivo README.md o en el Canvas "README - Guía de Despliegue Rápido").
(Una vez que el script finalice y muestre "CONFIGURACIÓN COMPLETADA", presione Enter si es necesario.)

Salir del Shell:
exit()

PASO 3: INICIO DEL SERVIDOR Y VERIFICACIÓN

Iniciar el servidor de desarrollo:
python manage.py runserver

Abrir el Navegador:
Acceder a la administración en: http://127.0.0.1:8000/admin/

Credenciales de Prueba (Contraseña para todos es: TheStrokes94):

Usuario: Patricia_Vidal (Super usuario)

Usuario: admin_gestor (Acceso total, puede eliminar)

Usuario: manager_user (Solo añade/edita Precio/Stock)

Usuario: viewer_only (Solo puede ver)

NOTA IMPORTANTE:

La lógica de permisos está definida en la clase ProductAdmin dentro de 'inventario/admin.py'.
El acceso de todos los usuarios de prueba fue configurado automáticamente con el estatus 'Es staff' y 'Activo' en el Paso 2.
