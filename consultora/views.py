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



from .models import Empresa
from .forms import EmpresaForm
from django.core.paginator import Paginator

def empresa_list(request):
    empresas = Empresa.objects.order_by('-fecha_creacion')
    paginator = Paginator(empresas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'empresas/empresa_list.html', {
        'empresas': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

def empresa_crear(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('empresa_list'))
    else:
        form = EmpresaForm()
    return render(request, 'empresas/empresa_form.html', {'form': form})

def empresa_editar(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect(reverse('empresa_list'))
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'empresas/empresa_form.html', {'form': form})


from .models import ServicioContable
from .forms import ServicioContableForm
from django.core.paginator import Paginator

def servicio_list(request):
    servicios = ServicioContable.objects.select_related('empresa').order_by('-fecha_inicio')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'servicios/servicio_list.html', {
        'servicios': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

def servicio_crear(request):
    if request.method == 'POST':
        form = ServicioContableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('servicio_list'))
    else:
        form = ServicioContableForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})

def servicio_editar(request, pk):
    servicio = get_object_or_404(ServicioContable, pk=pk)
    if request.method == 'POST':
        form = ServicioContableForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect(reverse('servicio_list'))
    else:
        form = ServicioContableForm(instance=servicio)
    return render(request, 'servicios/servicio_form.html', {'form': form})



from .models import Cuenta
from .forms import CuentaForm
from django.core.paginator import Paginator

def cuenta_list(request):
    cuentas = Cuenta.objects.select_related('cuenta_padre').order_by('codigo')
    paginator = Paginator(cuentas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cuentas/cuenta_list.html', {
        'cuentas': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

def cuenta_crear(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cuenta_list'))
    else:
        form = CuentaForm()
    return render(request, 'cuentas/cuenta_form.html', {'form': form})

def cuenta_editar(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk)
    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect(reverse('cuenta_list'))
    else:
        form = CuentaForm(instance=cuenta)
    return render(request, 'cuentas/cuenta_form.html', {'form': form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
from .models import AsientoDiario, LineaAsiento, Cuenta, Empresa
from .forms import AsientoDiarioForm, LineaAsientoFormSet


def seleccionar_empresa_asientos(request):
    empresas = Empresa.objects.all().order_by('razon_social')
    context = {
        'empresas': empresas,
        'title': 'Seleccionar Empresa'
    }
    return render(request, 'contabilidad/seleccionar_empresa_asientos.html', context)


def crear_asiento_diario(request, empresa_id):
    """
    Vista para crear un nuevo asiento diario con sus líneas
    """
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        form = AsientoDiarioForm(request.POST, empresa=empresa)
        
        if form.is_valid():
            # Crear el asiento pero no guardarlo aún
            asiento = form.save(commit=False)
            asiento.empresa = empresa
            
            # Generar número de asiento automáticamente
            mes_seleccionado = form.cleaned_data['mes']
            ultimo_numero = AsientoDiario.objects.filter(
                mes=mes_seleccionado,
                empresa=empresa
            ).order_by('-numero_asiento').first()
            
            asiento.numero_asiento = (ultimo_numero.numero_asiento + 1) if ultimo_numero else 1
            
            # Crear el formset de líneas
            formset = LineaAsientoFormSet(request.POST, instance=asiento)
            
            if formset.is_valid():
                # Validar que el asiento esté balanceado
                total_debe = Decimal('0')
                total_haber = Decimal('0')
                
                for form_linea in formset:
                    if form_linea.cleaned_data and not form_linea.cleaned_data.get('DELETE', False):
                        total_debe += form_linea.cleaned_data.get('debe', 0) or Decimal('0')
                        total_haber += form_linea.cleaned_data.get('haber', 0) or Decimal('0')
                
                if total_debe != total_haber:
                    messages.error(request, f'El asiento no está balanceado. Debe: {total_debe}, Haber: {total_haber}')
                else:
                    # Guardar en transacción
                    try:
                        with transaction.atomic():
                            asiento.save()
                            formset.save()
                        
                        messages.success(request, f'Asiento diario #{asiento.numero_asiento} creado exitosamente.')
                        return redirect('listar_asientos_diario', empresa_id=empresa.id)
                    
                    except Exception as e:
                        messages.error(request, f'Error al guardar el asiento: {str(e)}')
            else:
                messages.error(request, 'Por favor corrige los errores en las líneas del asiento.')
        else:
            formset = LineaAsientoFormSet()
    else:
        form = AsientoDiarioForm(empresa=empresa)
        formset = LineaAsientoFormSet()
    
    # Obtener cuentas para el selector dinámico
    cuentas = Cuenta.objects.all().order_by('codigo')
    
    context = {
        'form': form,
        'formset': formset,
        'empresa': empresa,
        'cuentas': cuentas,
        'title': 'Crear Asiento Diario'
    }
    
    return render(request, 'contabilidad/crear_asiento_diario.html', context)

def listar_asientos_diario(request, empresa_id):
    """
    Vista para listar todos los asientos diarios de una empresa
    """
    empresa = get_object_or_404(Empresa, id=empresa_id)
    asientos = AsientoDiario.objects.filter(empresa=empresa).order_by('-fecha', '-numero_asiento')
    
    context = {
        'asientos': asientos,
        'empresa': empresa,
        'title': 'Asientos Diario'
    }
    
    return render(request, 'contabilidad/listar_asientos_diario.html', context)

def detalle_asiento_diario(request, asiento_id):
    """
    Vista para ver el detalle de un asiento diario
    """
    asiento = get_object_or_404(AsientoDiario, id=asiento_id)
    lineas = asiento.lineas.all().order_by('cuenta__codigo')
    
    # Calcular totales
    total_debe = sum(linea.debe for linea in lineas)
    total_haber = sum(linea.haber for linea in lineas)
    
    context = {
        'asiento': asiento,
        'lineas': lineas,
        'total_debe': total_debe,
        'total_haber': total_haber,
        'title': f'Asiento #{asiento.numero_asiento}'
    }
    
    return render(request, 'contabilidad/detalle_asiento_diario.html', context)

def buscar_cuentas(request):
    """
    Vista AJAX para buscar cuentas por código o nombre
    """
    query = request.GET.get('q', '')
    cuentas = Cuenta.objects.filter(
        codigo__icontains=query
    ).values('id', 'codigo', 'nombre')[:10]
    
    return JsonResponse(list(cuentas), safe=False)









from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q, Sum
from .models import BalanceGeneral, BalanceGeneralLinea, Empresa, Cuenta
from .forms import (
    BalanceGeneralForm, 
    BalanceGeneralLineaForm, 
    BalanceGeneralLineaFormSet,
    BalanceGeneralFiltroForm
)


class BalanceGeneralListView(LoginRequiredMixin, ListView):
    model = BalanceGeneral
    template_name = 'balance/balance_list.html'
    context_object_name = 'balances'
    paginate_by = 10

    def get_queryset(self):
        queryset = BalanceGeneral.objects.select_related('empresa').prefetch_related('lineas')
        
        # Aplicar filtros
        empresa = self.request.GET.get('empresa')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if empresa:
            queryset = queryset.filter(empresa_id=empresa)
        if fecha_desde:
            queryset = queryset.filter(fecha_corte__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_corte__lte=fecha_hasta)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = BalanceGeneralFiltroForm(self.request.GET)
        return context


class BalanceGeneralDetailView(LoginRequiredMixin, DetailView):
    model = BalanceGeneral
    template_name = 'balance/balance_detail.html'
    context_object_name = 'balance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lineas = self.object.lineas.select_related('cuenta').order_by('cuenta__codigo')
        
        # Agrupar por tipo de cuenta para mejor visualización
        activos = lineas.filter(cuenta__tipo='ACTIVO')
        pasivos = lineas.filter(cuenta__tipo='PASIVO')
        patrimonio = lineas.filter(cuenta__tipo='PATRIMONIO')
        
        context.update({
            'lineas': lineas,
            'activos': activos,
            'pasivos': pasivos,
            'patrimonio': patrimonio,
            'total_activos': activos.aggregate(total=Sum('monto'))['total'] or 0,
            'total_pasivos': pasivos.aggregate(total=Sum('monto'))['total'] or 0,
            'total_patrimonio': patrimonio.aggregate(total=Sum('monto'))['total'] or 0,
        })
        return context


class BalanceGeneralCreateView(LoginRequiredMixin, CreateView):
    model = BalanceGeneral
    form_class = BalanceGeneralForm
    template_name = 'balance/balance_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = BalanceGeneralLineaFormSet(self.request.POST)
        else:
            context['formset'] = BalanceGeneralLineaFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                messages.success(self.request, f'Balance General creado exitosamente para {self.object.empresa.razon_social}')
                return redirect('balance:detail', pk=self.object.pk)
            else:
                messages.error(self.request, 'Por favor corrige los errores en las líneas del balance.')
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('balance:detail', kwargs={'pk': self.object.pk})


class BalanceGeneralUpdateView(LoginRequiredMixin, UpdateView):
    model = BalanceGeneral
    form_class = BalanceGeneralForm
    template_name = 'balance/balance_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = BalanceGeneralLineaFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = BalanceGeneralLineaFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.save()
                messages.success(self.request, 'Balance General actualizado exitosamente.')
                return redirect('balance:detail', pk=self.object.pk)
            else:
                messages.error(self.request, 'Por favor corrige los errores en las líneas del balance.')
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('balance:detail', kwargs={'pk': self.object.pk})


class BalanceGeneralDeleteView(LoginRequiredMixin, DeleteView):
    model = BalanceGeneral
    template_name = 'balance/balance_confirm_delete.html'
    success_url = reverse_lazy('balance:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Balance General eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Vista AJAX para obtener cuentas por empresa
def get_cuentas_por_empresa(request):
    empresa_id = request.GET.get('empresa_id')
    if empresa_id:
        cuentas = Cuenta.objects.filter(empresa_id=empresa_id).order_by('codigo')
        data = [{'id': cuenta.id, 'codigo': cuenta.codigo, 'nombre': cuenta.nombre} 
                for cuenta in cuentas]
        return JsonResponse({'cuentas': data})
    return JsonResponse({'cuentas': []})









# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import LibroMayor, LibroMayorLinea
from .forms import LibroMayorForm, LibroMayorLineaForm, LibroMayorFiltroForm

class LibroMayorListView(ListView):
    model = LibroMayor
    template_name = 'libro_mayor/libro_mayor_list.html'
    context_object_name = 'libros_mayores'
    paginate_by = 20

    def get_queryset(self):
        queryset = LibroMayor.objects.select_related('empresa', 'cuenta')
        
        # Aplicar filtros
        empresa = self.request.GET.get('empresa')
        cuenta = self.request.GET.get('cuenta')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        search = self.request.GET.get('search')

        if empresa:
            queryset = queryset.filter(empresa_id=empresa)
        
        if cuenta:
            queryset = queryset.filter(cuenta_id=cuenta)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_inicio__gte=fecha_desde)
        
        if fecha_hasta:
            queryset = queryset.filter(fecha_fin__lte=fecha_hasta)
        
        if search:
            queryset = queryset.filter(
                Q(empresa__razon_social__icontains=search) |
                Q(cuenta__nombre__icontains=search) |
                Q(cuenta__codigo__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = LibroMayorFiltroForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class LibroMayorCreateView(CreateView):
    model = LibroMayor
    form_class = LibroMayorForm
    template_name = 'libro_mayor/libro_mayor_create.html'
    success_url = reverse_lazy('libro_mayor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Libro Mayor creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el Libro Mayor. Revisa los datos ingresados.')
        return super().form_invalid(form)

class LibroMayorDetailView(DetailView):
    model = LibroMayor
    template_name = 'libro_mayor/libro_mayor_detail.html'
    context_object_name = 'libro_mayor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener líneas del libro mayor con paginación
        lineas = self.object.lineas.select_related('asiento', 'linea_asiento').order_by('fecha', 'id')
        paginator = Paginator(lineas, 50)
        page_number = self.request.GET.get('page')
        context['lineas_page'] = paginator.get_page(page_number)
        
        # Calcular totales
        context['total_debe'] = sum(linea.debe for linea in lineas)
        context['total_haber'] = sum(linea.haber for linea in lineas)
        context['saldo_final'] = lineas.last().saldo_acumulado if lineas.exists() else 0
        
        return context

# Vistas para LibroMayorLinea
class LibroMayorLineaListView(ListView):
    model = LibroMayorLinea
    template_name = 'libro_mayor/linea_list.html'
    context_object_name = 'lineas'
    paginate_by = 50

    def get_queryset(self):
        libro_id = self.kwargs.get('libro_id')
        if libro_id:
            return LibroMayorLinea.objects.filter(libro_id=libro_id).select_related('asiento', 'linea_asiento')
        return LibroMayorLinea.objects.select_related('libro', 'asiento', 'linea_asiento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro_id = self.kwargs.get('libro_id')
        if libro_id:
            context['libro_mayor'] = get_object_or_404(LibroMayor, pk=libro_id)
        return context

class LibroMayorLineaCreateView(CreateView):
    model = LibroMayorLinea
    form_class = LibroMayorLineaForm
    template_name = 'libro_mayor/linea_create.html'

    def get_success_url(self):
        if self.object.libro:
            return reverse_lazy('libro_mayor_detail', kwargs={'pk': self.object.libro.pk})
        return reverse_lazy('libro_mayor_list')

    def get_initial(self):
        initial = super().get_initial()
        libro_id = self.kwargs.get('libro_id')
        if libro_id:
            initial['libro'] = libro_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Línea de Libro Mayor creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la línea. Revisa los datos ingresados.')
        return super().form_invalid(form)