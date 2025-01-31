from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ImobiliariaUser, NormalUser

# Registrar o CustomUser com o UserAdmin personalizado (opcional)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo_usuario')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo_usuario',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ImobiliariaUser)
admin.site.register(NormalUser)