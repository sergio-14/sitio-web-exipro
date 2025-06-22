from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-700 dark:text-white'
            }),
        }

class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Correo Electrónico',
            'class': 'w-full px-3 py-2 rounded border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-700 dark:text-white'
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'w-full px-3 py-2 rounded border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-700 dark:text-white'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_attempt = True

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                self.first_attempt = False
                if not User.objects.filter(email=email).exists():
                    self.add_error('email', "El correo electrónico no existe.")
                else:
                    self.add_error('password', "La contraseña es incorrecta.")
            elif not user.is_active:
                self.first_attempt = False
                raise forms.ValidationError("Esta cuenta está inactiva.")
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = User
        fields = (
            'email', 'nombre', 'apellido', 'apellidoM', 'dni', 'telefono', 'direccion',
            'imagen',
            'is_active', 'is_staff', 'is_superuser',
            'password1', 'password2', 'groups'
        )
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-tw'}),
            'nombre': forms.TextInput(attrs={'class': 'input-tw'}),
            'apellido': forms.TextInput(attrs={'class': 'input-tw'}),
            'apellidoM': forms.TextInput(attrs={'class': 'input-tw'}),
            'dni': forms.TextInput(attrs={'class': 'input-tw'}),
            'telefono': forms.TextInput(attrs={'class': 'input-tw'}),
            'direccion': forms.TextInput(attrs={'class': 'input-tw'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'file-input-tw'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox-tw', 'id': 'flexSwitchCheckActive'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'checkbox-tw', 'id': 'flexSwitchCheckStaff'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'checkbox-tw', 'id': 'flexSwitchCheckSuperuser'}),
            'password1': forms.PasswordInput(attrs={'class': 'input-tw'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-tw'}),
        }
        labels = {
            'dni': 'Carnet de Identidad',
            'apellido': 'Apellido Paterno',
            'apellidoM': 'Apellido Materno',
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError(_("La contraseña debe tener al menos 8 caracteres."))
        if not any(char.isupper() for char in password1):
            raise ValidationError(_("La contraseña debe contener al menos una mayúscula."))
        if password1.isdigit():
            raise ValidationError(_("La contraseña no puede consistir solo en números."))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Las contraseñas no coinciden."))
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Ya existe un usuario con este correo electrónico."))
        return email

    def get_available_groups(self):
        return Group.objects.exclude(id__in=self.instance.groups.values_list('id', flat=True))


class CustomUserChangeForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'apellidoM', 'imagen','dni', 'telefono', 'direccion', 'is_active', 'is_staff','is_superuser', 'groups')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-tw'}),
            'nombre': forms.TextInput(attrs={'class': 'input-tw'}),
            'apellido': forms.TextInput(attrs={'class': 'input-tw'}),
            'apellidoM': forms.TextInput(attrs={'class': 'input-tw'}),
            'telefono': forms.TextInput(attrs={'class': 'input-tw'}),
            'direccion': forms.TextInput(attrs={'class': 'input-tw'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'file-input-tw'}),
            'dni': forms.TextInput(attrs={'class': 'input-tw'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox-tw', 'id': 'flexSwitchCheckActive'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'checkbox-tw', 'id': 'flexSwitchCheckStaff'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'checkbox-tw', 'id': 'flexSwitchCheckSuperuser'}),
        }
        labels = {
            'apellido': 'Apellido Paterno',
            'apellidoM': 'Apellido Materno',
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'nombre', 'apellido', 'apellidoM', 'telefono', 'direccion', 'imagen']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-tw'}),
            'nombre': forms.TextInput(attrs={'class': 'input-tw'}),
            'apellido': forms.TextInput(attrs={'class': 'input-tw'}),
            'apellidoM': forms.TextInput(attrs={'class': 'input-tw'}),
            'telefono': forms.TextInput(attrs={'class': 'input-tw'}),
            'direccion': forms.TextInput(attrs={'class': 'input-tw'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'file-input-tw'}),
        }

from .models import Curso,Categoria

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo','descripcion_breve', 'descripcion_completa','imagen_portada', 'precio', 'es_gratuito','fecha_publicacion', 'instructor', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-tw', 'placeholder': 'Título del curso'}),
            'descripcion_breve': forms.Textarea(attrs={'class': 'input-tw', 'rows': 3, 'placeholder': 'Descripción breve'}),
            'descripcion_completa': forms.Textarea(attrs={'class': 'input-tw', 'rows': 6, 'placeholder': 'Descripción completa'} ),
            'imagen_portada': forms.ClearableFileInput(attrs={'class': 'file-input-tw'} ),
            'precio': forms.NumberInput( attrs={'class': 'input-tw', 'step': '0.01'} ),
            'es_gratuito': forms.CheckboxInput( attrs={'class': 'checkbox-tw'} ),
            'fecha_publicacion': forms.DateTimeInput(attrs={'class': 'input-tw','type': 'datetime-local' } ),
            'instructor': forms.Select( attrs={'class': 'input-tw'}),
            'categoria': forms.Select(  attrs={'class': 'input-tw'}),
        }
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-tw', 'placeholder': 'Nombre de Categoria'}),
        }
        
        
from .models import Modulo


        
from django import forms
from django.forms import inlineformset_factory
from .models import Modulo, Leccion

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'orden', 'curso']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-tw', 'placeholder': 'Título del módulo'}),
            'orden': forms.NumberInput(attrs={'class': 'input-tw'}),
            'curso': forms.Select(attrs={'class': 'input-tw'}),
        }

class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = ['titulo', 'descripcion', 'tipo_contenido', 'url_contenido', 'duracion_minutos', 'orden']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-tw', 'placeholder': 'Título de la lección'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-tw', 'rows': 2, 'placeholder': 'Descripción'}),
            'tipo_contenido': forms.TextInput(attrs={'class': 'input-tw', 'placeholder': 'Tipo de contenido'}),
            'url_contenido': forms.URLInput(attrs={'class': 'input-tw', 'placeholder': 'URL del contenido'}),
            'duracion_minutos': forms.NumberInput(attrs={'class': 'input-tw'}),
            'orden': forms.NumberInput(attrs={'class': 'input-tw'}),
        }

LeccionFormSet = inlineformset_factory(
    Modulo, Leccion, form=LeccionForm,
    extra=1, can_delete=True
)

from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razon_social', 'nit', 'direccion', 'telefono', 'email']
        widgets = {
            'razon_social': forms.TextInput(attrs={
                'class': 'input-tw',
                'placeholder': 'Razón social'
            }),
            'nit': forms.TextInput(attrs={
                'class': 'input-tw',
                'placeholder': 'NIT'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'input-tw',
                'placeholder': 'Dirección'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'input-tw',
                'placeholder': 'Teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-tw',
                'placeholder': 'Correo electrónico'
            }),
        }
        

from .models import ServicioContable

class ServicioContableForm(forms.ModelForm):
    class Meta:
        model = ServicioContable
        fields = ['empresa', 'empleados', 'fecha_inicio', 'fecha_fin', 'activo']
        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'input-tw'
            }),
            'empleados': forms.SelectMultiple(attrs={
                'class': 'input-tw'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'input-tw',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'input-tw',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'checkbox-tw'
            }),
        }



from django import forms
from .models import Cuenta

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['codigo', 'nombre', 'tipo', 'nivel', 'cuenta_padre']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'input-tw',
                'placeholder': 'Ej. 1.01.05'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'input-tw',
                'placeholder': 'Nombre de la cuenta'
            }),
            'tipo': forms.Select(attrs={
                'class': 'input-tw'
            }),
            'nivel': forms.NumberInput(attrs={
                'class': 'input-tw',
                'min': 1
            }),
            'cuenta_padre': forms.Select(attrs={
                'class': 'input-tw'
            }),
            
        }



from django import forms
from django.forms import inlineformset_factory
from .models import AsientoDiario, LineaAsiento, Cuenta, Glosa, Mes
from decimal import Decimal

class AsientoDiarioForm(forms.ModelForm):
    class Meta:
        model = AsientoDiario
        fields = ['fecha', 'glosa', 'mes']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white'
                }
            ),
            'glosa': forms.Select(
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white'
                }
            ),
            'mes': forms.Select(
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        
        if empresa:
            self.fields['mes'].queryset = Mes.objects.filter(
                empresa=empresa, 
                abierto=True
            ).order_by('-ano', '-mes')
        
        # Agregar opción vacía para glosa
        self.fields['glosa'].empty_label = "Seleccionar glosa (opcional)"

class LineaAsientoForm(forms.ModelForm):
    class Meta:
        model = LineaAsiento
        fields = ['cuenta', 'descripcion', 'debe', 'haber']
        widgets = {
            'cuenta': forms.Select(
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white text-sm'
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white text-sm',
                    'placeholder': 'Descripción opcional'
                }
            ),
            'debe': forms.NumberInput(
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white text-sm text-right',
                    'step': '0.01',
                    'min': '0',
                    'placeholder': '0.00'
                }
            ),
            'haber': forms.NumberInput(
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-700 dark:text-white text-sm text-right',
                    'step': '0.01',
                    'min': '0',
                    'placeholder': '0.00'
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        debe = cleaned_data.get('debe', 0)
        haber = cleaned_data.get('haber', 0)
        
        # Convertir a Decimal si son strings
        if isinstance(debe, str):
            debe = Decimal(debe) if debe else Decimal('0')
        if isinstance(haber, str):
            haber = Decimal(haber) if haber else Decimal('0')
            
        # Validar que no ambos sean cero
        if debe == 0 and haber == 0:
            raise forms.ValidationError("Debe o Haber debe tener un valor mayor a cero.")
        
        # Validar que no ambos tengan valor
        if debe > 0 and haber > 0:
            raise forms.ValidationError("Solo puede tener valor en Debe O en Haber, no en ambos.")
            
        return cleaned_data

# Formset para manejar múltiples líneas de asiento
LineaAsientoFormSet = inlineformset_factory(
    AsientoDiario, 
    LineaAsiento,
    form=LineaAsientoForm,
    extra=0,  # Líneas adicionales vacías
    can_delete=True,
    min_num=1,  # Mínimo 2 líneas (debe y haber)
    validate_min=True
)



from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import BalanceGeneral, BalanceGeneralLinea, Empresa, Cuenta


class BalanceGeneralForm(forms.ModelForm):
    class Meta:
        model = BalanceGeneral
        fields = ['empresa', 'fecha_corte']
        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'fecha_corte': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
        }
        labels = {
            'empresa': 'Empresa',
            'fecha_corte': 'Fecha de Corte',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.all()
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': f'Seleccione {field.label.lower()}'
            })


class BalanceGeneralLineaForm(forms.ModelForm):
    class Meta:
        model = BalanceGeneralLinea
        fields = ['cuenta', 'monto']
        widgets = {
            'cuenta': forms.Select(attrs={
                'class': 'w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm transition-all duration-200'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm transition-all duration-200',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuenta'].queryset = Cuenta.objects.all().order_by('codigo')
        self.fields['monto'].widget.attrs.update({'min': '0'})


class BalanceGeneralFiltroForm(forms.Form):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=False,
        empty_label="Todas las empresas",
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
        })
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
        })
    )


# Formset para manejo múltiple de líneas
BalanceGeneralLineaFormSet = inlineformset_factory(
    BalanceGeneral,
    BalanceGeneralLinea,
    form=BalanceGeneralLineaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)





# forms.py
from django import forms
from django.utils import timezone
from .models import LibroMayor, LibroMayorLinea, Empresa, Cuenta

class LibroMayorForm(forms.ModelForm):
    class Meta:
        model = LibroMayor
        fields = ['empresa', 'cuenta', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'cuenta': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = timezone.now().date()
        self.fields['fecha_fin'].required = False
        
        # Añadir clases de ayuda
        self.fields['empresa'].help_text = "Selecciona la empresa para el libro mayor"
        self.fields['cuenta'].help_text = "Selecciona la cuenta contable"
        self.fields['fecha_inicio'].help_text = "Fecha de inicio del período"
        self.fields['fecha_fin'].help_text = "Fecha de fin del período (opcional)"

class LibroMayorLineaForm(forms.ModelForm):
    class Meta:
        model = LibroMayorLinea
        fields = ['libro', 'asiento', 'linea_asiento', 'fecha', 'descripcion', 'debe', 'haber']
        widgets = {
            'libro': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'asiento': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'linea_asiento': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100',
                'placeholder': 'Descripción del movimiento'
            }),
            'debe': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100',
                'step': '0.01',
                'min': '0'
            }),
            'haber': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100',
                'step': '0.01',
                'min': '0'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].initial = timezone.now().date()
        self.fields['debe'].initial = 0
        self.fields['haber'].initial = 0

class LibroMayorFiltroForm(forms.Form):
    """Formulario para filtrar libros mayores"""
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=False,
        empty_label="Todas las empresas",
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
        })
    )
    
    cuenta = forms.ModelChoiceField(
        queryset=Cuenta.objects.all(),
        required=False,
        empty_label="Todas las cuentas",
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
        })
    )