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

    
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)