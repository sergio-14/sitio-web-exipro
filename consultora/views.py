from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm, UserForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
#vistas globales
def home (request):
    return render(request, 'home.html')


def dashboard (request):
    return render(request, 'dashboard.html')

#@login_required
def lista_usuarios(request):
    query = request.GET.get('q')
    usuarios = User.objects.all()

    if query:
        usuarios = usuarios.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(apellidoM__icontains=query)
        )

    paginator = Paginator(usuarios, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'usuarios/lista_usuarios.html', context)

#@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/form_usuarios.html', {'form': form, 'titulo': 'Agregar Usuario'})

#@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)
    return render(request, 'usuarios/form_usuarios.html', {'form': form, 'titulo': 'Editar Usuario'})

#@login_required
def deshabilitar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = False
    usuario.save()
    messages.warning(request, "Usuario deshabilitado correctamente.")
    return redirect('lista_usuarios')

#@login_required
def activar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = True
    usuario.save()
    return redirect('lista_usuarios')



def iniciar_sesion(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            # Verificar si los campos están vacíos
            if form.cleaned_data.get('email') or form.cleaned_data.get('password'):
                form.first_attempt = False
            else:
                form.first_attempt = True
    else:
        form = CustomLoginForm()
    return render(request, 'IniciarSesion.html', {'form': form})


# Cerrar Sesión
def signout(request):
    logout(request)
    return redirect('home')




#cursos todp
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Curso
from .forms import CursoForm

def curso_list(request):
    query = request.GET.get('q', '')
    cursos = Curso.objects.all()
    if query:
        cursos = cursos.filter(titulo__icontains=query)
    cursos = cursos.order_by('-fecha_publicacion')
    
    paginator = Paginator(cursos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cursos/curso_list.html', {
        'cursos': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'query': query,
    })

def curso_crear(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.save()
            return redirect('curso_list')
    else:
        form = CursoForm()
    return render(request, 'cursos/curso_form.html', {
        'form': form,
        'titulo': 'Agregar Curso',
    })

def curso_editar(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.save()
            return redirect('curso_list')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/curso_form.html', {
        'form': form,
        'titulo': 'Editar Curso',
    })
    
from .models import Categoria
from .forms import CategoriaForm
from django.core.paginator import Paginator

def categoria_list(request):
    query = request.GET.get('q')
    categorias = Categoria.objects.all()
    if query:
        categorias = categorias.filter(nombre__icontains=query)
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categorias/categoria_list.html', {
        'categorias': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': page_obj.has_other_pages(),
    })

def categoria_crear(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('categoria_list')
    return render(request, 'categorias/categoria_form.html', {'form': form, 'titulo': 'Agregar Categoría'})

def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('categoria_list')
    return render(request, 'categorias/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})



from .models import Modulo
from .forms import ModuloForm

"""def modulo_list(request):
    modulos = Modulo.objects.select_related('curso').prefetch_related('lecciones').all()
    return render(request, 'modulos/modulo_list.html', {
        'modulos': modulos,
        'titulo': 'Listado de Módulos y Lecciones',
    })
"""
"""def modulo_list(request):
    modulos = Modulo.objects.select_related('curso').order_by('curso', 'orden')
    return render(request, 'modulos/modulo_list.html', {'modulos': modulos})"""

def modulo_crear(request):
    form = ModuloForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('modulo_list')
    return render(request, 'modulos/modulo_form.html', {'form': form, 'titulo': 'Agregar Módulo'})

def modulo_editar(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    form = ModuloForm(request.POST or None, instance=modulo)
    if form.is_valid():
        form.save()
        return redirect('modulo_list')
    return render(request, 'modulos/modulo_form.html', {'form': form, 'titulo': 'Editar Módulo'})


from .forms import ModuloForm, LeccionFormSet

"""def modulo_con_lecciones_crear(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        formset = LeccionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            modulo = form.save()
            lecciones = formset.save(commit=False)
            for leccion in lecciones:
                leccion.modulo = modulo
                leccion.save()
            return redirect('modulo_list')
    else:
        form = ModuloForm()
        formset = LeccionFormSet()
    
    return render(request, 'modulos/modulo_form_completo.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Agregar Módulo y Lecciones',
    })"""
    
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Modulo, Leccion, Curso
from .forms import ModuloForm, LeccionForm

def modulo_con_lecciones_crear(request):
    LeccionFormSet = inlineformset_factory(
        Modulo, 
        Leccion, 
        form=LeccionForm,
        extra=1,  # Al menos una lección vacía
        can_delete=True,
        can_delete_extra=True
    )
    
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        formset = LeccionFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            modulo = form.save()
            lecciones = formset.save(commit=False)
            
            # Asignar el módulo a cada lección
            for leccion in lecciones:
                leccion.modulo = modulo
                leccion.save()
            
            # Eliminar lecciones marcadas para eliminar
            formset.save_m2m()
            
            messages.success(request, f'Módulo "{modulo.titulo}" creado exitosamente con {len(lecciones)} lecciones.')
            return redirect('modulo_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ModuloForm()
        formset = LeccionFormSet()

    return render(request, 'modulos/modulo_form_completo.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Crear Módulo con Lecciones',
        'action': 'crear'
    })

def modulo_con_lecciones_editar(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    LeccionFormSet = inlineformset_factory(
        Modulo, 
        Leccion, 
        form=LeccionForm,
        extra=0,  # No agregar formularios extra en edición
        can_delete=True
    )
    
    if request.method == 'POST':
        form = ModuloForm(request.POST, instance=modulo)
        formset = LeccionFormSet(request.POST, instance=modulo)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            messages.success(request, f'Módulo "{modulo.titulo}" actualizado exitosamente.')
            return redirect('modulo_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ModuloForm(instance=modulo)
        formset = LeccionFormSet(instance=modulo)

    return render(request, 'modulos/modulo_form_completo.html', {
        'form': form,
        'formset': formset,
        'titulo': f'Editar Módulo: {modulo.titulo}',
        'action': 'editar',
        'modulo': modulo
    })

def modulo_list(request):
    query = request.GET.get("q")
    modulos = Modulo.objects.select_related('curso').prefetch_related('lecciones')

    if query:
        modulos = modulos.filter(curso__titulo__icontains=query)

    total_modulos = modulos.count()
    total_lecciones = sum(modulo.lecciones.count() for modulo in modulos)

    context = {
        'modulos': modulos,
        'titulo': 'Gestión de Módulos',
        'total_modulos': total_modulos,
        'total_lecciones': total_lecciones,
        'query': query,
    }
    return render(request, 'modulos/modulo_list.html', context)



def modulo_detalle(request, pk):
    modulo = get_object_or_404(Modulo.objects.select_related('curso').prefetch_related('lecciones'), pk=pk)
    
    context = {
        'modulo': modulo,
        'titulo': f'Detalle: {modulo.titulo}',
    }
    return render(request, 'modulos/modulo_detalle.html', context)

"""def modulo_eliminar(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    
    if request.method == 'POST':
        titulo = modulo.titulo
        modulo.delete()
        messages.success(request, f'Módulo "{titulo}" eliminado exitosamente.')
        return redirect('modulo_list')
    
    context = {
        'modulo': modulo,
        'titulo': f'Eliminar Módulo: {modulo.titulo}',
    }
    return render(request, 'modulos/modulo_confirmar_eliminar.html', context)"""

