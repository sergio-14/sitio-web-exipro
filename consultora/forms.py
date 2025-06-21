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
