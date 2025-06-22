"""
URL configuration for administrador project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from consultora import views

urlpatterns = [
    #area de vista general
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard' ),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.signout, name='logout'),
    
    #usuarios 
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/activar/<int:pk>/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/deshabilitar/<int:pk>/', views.deshabilitar_usuario, name='deshabilitar_usuario'),
    
    #categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/agregar/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),

    
    #cursos 
    path('cursos/', views.curso_list, name='curso_list'),
    path('cursos/agregar/', views.curso_crear, name='curso_crear'),
    path('cursos/<int:pk>/editar/', views.curso_editar, name='curso_editar'),
    
    #modulos
    #path('modulos/', views.modulo_list, name='modulo_list'),
    path('}hola/', views.modulo_crear, name='modulo_crear'),
    path('modulos/<int:pk>/editar/', views.modulo_editar, name='modulo_editar'),
    
    
    #path('modulos/agregar/', views.modulo_con_lecciones_crear, name='modulo_con_lecciones_crear'),
    
    path('modulos/', views.modulo_list, name='modulo_list'),
    
    # Crear módulo con lecciones
    path('modulos/crear/', views.modulo_con_lecciones_crear, name='modulo_con_lecciones_crear'),
    
    # Editar módulo con lecciones
    path('modulos/<int:pk>/editar/', views.modulo_con_lecciones_editar, name='modulo_con_lecciones_editar'),
    
    # Ver detalle del módulo
    path('modulos/<int:pk>/', views.modulo_detalle, name='modulo_detalle'),
    
    # Eliminar módulo
    #path('modulos/<int:pk>/eliminar/', views.modulo_eliminar, name='modulo_eliminar'),
    
    
    
    #area de contabilidad 
    
    #empresa 
    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresas/agregar/', views.empresa_crear, name='empresa_crear'),
    path('empresas/<int:pk>/editar/', views.empresa_editar, name='empresa_editar'),
    
    #asignacion servicios
    path('servicios/', views.servicio_list, name='servicio_list'),
    path('servicios/agregar/', views.servicio_crear, name='servicio_crear'),
    path('servicios/<int:pk>/editar/', views.servicio_editar, name='servicio_editar'),
    
    
    #plan de cuentas
    path('cuentas/', views.cuenta_list, name='cuenta_list'),
    path('cuentas/agregar/', views.cuenta_crear, name='cuenta_crear'),
    path('cuentas/<int:pk>/editar/', views.cuenta_editar, name='cuenta_editar'),
    
    
    
    path('empresa/<int:empresa_id>/asientos/', views.listar_asientos_diario, name='listar_asientos_diario'),
    path('empresa/<int:empresa_id>/asientos/crear/', views.crear_asiento_diario, name='crear_asiento_diario'),
    path('asientos/<int:asiento_id>/', views.detalle_asiento_diario, name='detalle_asiento_diario'),
    path('asientos/', views.seleccionar_empresa_asientos, name='seleccionar_empresa_asientos'),
    # AJAX
    path('api/buscar-cuentas/', views.buscar_cuentas, name='buscar_cuentas'),
    
    
    
    
    # Lista de balances
    path('balance/lista', views.BalanceGeneralListView.as_view(), name='balance_list'),
    
    # Detalle de balance
    path('balance/<int:pk>/detalle/', views.BalanceGeneralDetailView.as_view(), name='balance_detail'),
    
    # Crear balance
    path('balance/crear/', views.BalanceGeneralCreateView.as_view(), name='balance_create'),
    
    # Editar balance
    path('balance/<int:pk>/editar/', views.BalanceGeneralUpdateView.as_view(), name='balance_update'),
    
    # Eliminar balance
   # path('<int:pk>/eliminar/', views.BalanceGeneralDeleteView.as_view(), name='delete'),
    
    # API endpoints
    #path('api/cuentas/', views.get_cuentas_por_empresa, name='api_cuentas'),
  
  
  
  
  
    path('libro_mayor/', views.LibroMayorListView.as_view(), name='libro_mayor_list'),
    
    # Crear libro mayor
    path('libro_mayor/crear/', views.LibroMayorCreateView.as_view(), name='libro_mayor_create'),
    
    # Ver detalle del libro mayor
    path('libro_mayor/<int:pk>/', views.LibroMayorDetailView.as_view(), name='libro_mayor_detail'),
    
    
    
    
    
    # Editar libro mayor
    #path('libro_mayor/<int:pk>/editar/', views.LibroMayorUpdateView.as_view(), name='libro_mayor_update'),
    
    # Eliminar libro mayor
    #path('libro_mayor/<int:pk>/eliminar/', views.LibroMayorDeleteView.as_view(), name='libro_mayor_delete'),
    
    # Agregar línea de asiento
    #path('libro_mayor/<int:pk>/agregar-linea/', views.AgregarLineaAsientoView.as_view(), name='agregar_linea_asiento'),
    
    # Editar línea de asiento
    #path('libro_mayor/linea/<int:pk>/editar/', views.EditarLineaAsientoView.as_view(), name='editar_linea_asiento'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)