from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponseRedirect
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

# Unregister the original Group admin to avoid redundancy
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'nombre', 'apellido', 'apellidoM',  'get_groups', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nombre', 'apellido', )
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre', 'apellido','apellidoM', 'imagen', 'dni', 'telefono')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido','apellidoM', 'is_active', 'is_staff', 'is_superuser', 'password1', 'password2', 'groups'),
        }),
    )

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupo'

    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" in request.POST:
            return super().response_add(request, obj, post_url_continue)
        return HttpResponseRedirect('/admin/usuarios/user/')

admin.site.register(User, CustomUserAdmin)


from .models import Categoria, Curso, Modulo, Leccion, Plan, Suscripcion, Pago, CursoCompra, Matricula, Empresa, ServicioContable, Cuenta, Mes, Glosa, AsientoDiario, LineaAsiento, LibroMayorEntry, BalanceGeneral, BalanceGeneralLinea, PeriodoFiscal, AsientoAjuste, AsientoAjusteLinea, CierreMensual

admin.site.register(Categoria)
admin.site.register(Curso) 
admin.site.register(Modulo)
admin.site.register(Leccion)
admin.site.register(Plan)
admin.site.register(Suscripcion)
admin.site.register(Pago)
admin.site.register(CursoCompra)
admin.site.register(Matricula)
admin.site.register(Empresa)
admin.site.register(ServicioContable)
admin.site.register(Cuenta)
admin.site.register(Mes)
admin.site.register(Glosa)
admin.site.register(AsientoDiario)
admin.site.register(LineaAsiento)
admin.site.register(LibroMayorEntry)
admin.site.register(BalanceGeneral)
admin.site.register(BalanceGeneralLinea)
admin.site.register(PeriodoFiscal)
admin.site.register(AsientoAjuste)
admin.site.register(AsientoAjusteLinea)
admin.site.register(CierreMensual)