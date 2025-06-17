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

