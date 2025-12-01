from django.contrib import admin
from .models import Product

ADMINISTRATORS_GROUP = "Administradores"
MANAGERS_GROUP = "Gestores_de_Productos"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('created_at', 'stock')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')
    fields = ('name', 'description', 'price', 'stock')
    
    def _is_in_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists()

    # Controla el permiso de AÑADIR (Crear)
    # Permite a Superusuarios y Gestores.
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return self._is_in_group(request.user, MANAGERS_GROUP)

    # Controla el permiso de CAMBIAR (Editar/Modificar)
    # Permite a Superusuarios, Administradores y Gestores.
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (self._is_in_group(request.user, ADMINISTRATORS_GROUP) or
                self._is_in_group(request.user, MANAGERS_GROUP))

    # Controla el permiso de ELIMINAR
    # Solo Superusuarios y Administradores pueden eliminar.
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return self._is_in_group(request.user, ADMINISTRATORS_GROUP)

    # Controla el permiso de VER
    # Permite ver a todos los usuarios que sean staff (para acceder al listado).
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
        
    # Mejoramos la UX: Gestores solo pueden editar Stock y Precio
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or self._is_in_group(request.user, ADMINISTRATORS_GROUP):
            return ()
        
        if self._is_in_group(request.user, MANAGERS_GROUP):
            return ('name', 'description', 'created_at')
            
        # Usuarios con solo permiso de vista (sin grupo asignado), no pueden editar nada.
        return ('name', 'description', 'price', 'stock', 'created_at')