from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group, Permission
from django.db import models
from django.utils import timezone
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.text import slugify




class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo de correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    imagen = models.ImageField(upload_to='Perfil/', null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    apellidoM = models.CharField(max_length=50, null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='Carnet Identidad:')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
 
    # Añade los campos para las relaciones de grupos y permisos
    groups = models.ManyToManyField(Group, blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permissions')
    
    # Campos para la fecha de creación y modificación
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido} {self.apellidoM}'


# ---------------------------------------------------
# 1. Categorías
# ---------------------------------------------------
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


# ---------------------------------------------------
# 2. Cursos
# ---------------------------------------------------
class Curso(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion_breve = models.TextField(blank=True, null=True)
    descripcion_completa = models.TextField(blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    es_gratuito = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)

    # Relación con instructor (usuario). Si el usuario se borra, se deja en NULL.
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cursos'
    )
    # Relación con categoría. Si la categoría se borra, se deja en NULL.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cursos'
    )
    
    def __str__(self):
        return self.titulo
    
    


# ---------------------------------------------------
# 3. Módulos
# ---------------------------------------------------
class Modulo(models.Model):
    titulo = models.CharField(max_length=150)
    orden = models.PositiveIntegerField()
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='modulos'
    )

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.curso.titulo} - Módulo {self.orden}: {self.titulo}"


# ---------------------------------------------------
# 4. Lecciones
# ---------------------------------------------------
class Leccion(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    tipo_contenido = models.CharField(
        max_length=20,
        help_text="p.ej. 'video', 'texto', 'pdf', etc."
    )
    url_contenido = models.URLField(max_length=255)
    duracion_minutos = models.PositiveIntegerField(blank=True, null=True)
    orden = models.PositiveIntegerField()
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='lecciones'
    )

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.modulo.titulo} - Lección {self.orden}: {self.titulo}"


# ---------------------------------------------------
# 5. Planes
# ---------------------------------------------------
class Plan(models.Model):
    nombre = models.CharField(max_length=50)
    duracion_dias = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.duracion_dias} días) - ${self.precio}"


# ---------------------------------------------------
# 6. Suscripciones
# ---------------------------------------------------
class Suscripcion(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('vencida', 'Vencida'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='suscripciones'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='suscripciones'
    )
    fecha_inicio = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.usuario.email} → {self.plan.nombre} ({self.estado})"


# ---------------------------------------------------
# 7. Pagos
# ---------------------------------------------------
class Pago(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('exito', 'Éxito'),
        ('pendiente', 'Pendiente'),
        ('fallido', 'Fallido'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='pagos'
    )
    suscripcion = models.ForeignKey(
        Suscripcion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos'
    )  # Si es NULL, puede ser pago único de curso
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)  # ’Tarjeta’, ’PayPal’, ’Stripe’, etc.
    fecha_pago = models.DateTimeField(default=timezone.now)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES)
    referencia_externa = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        susc = f"Suscripción ID {self.suscripcion.id}" if self.suscripcion else "PagoÚnico"
        return f"{self.usuario.email} → ${self.monto} ({self.estado_pago}) [{susc}]"


# ---------------------------------------------------
# 8. Compra única de curso
# ---------------------------------------------------
class CursoCompra(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compras_curso'
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='compras'
    )
    pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,
        related_name='compras_curso'
    )
    fecha_compra = models.DateTimeField(auto_now_add=True)
    acceso_hasta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.email} → {self.curso.titulo} (hasta {self.acceso_hasta})"


# ---------------------------------------------------
# 9. Matrículas
# ---------------------------------------------------
class Matricula(models.Model):
    TIPO_ACCESO_CHOICES = [
        ('suscripcion', 'Suscripción'),
        ('compra_unica', 'Compra Única'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matriculas'
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='matriculas'
    )
    fecha_matricula = models.DateTimeField(auto_now_add=True)
    tipo_acceso = models.CharField(max_length=20, choices=TIPO_ACCESO_CHOICES)

    def __str__(self):
        return f"{self.usuario.email} inscrito en {self.curso.titulo} ({self.tipo_acceso})"


# ------------------------------------------------------------
# 0. Empresa y Servicio Contable
# ------------------------------------------------------------

class Empresa(models.Model):
    """
    Representa a una empresa a la que se le brinda servicio contable.
    """
    razon_social = models.CharField(max_length=255, unique=True)
    nit = models.CharField(max_length=50, unique=True, verbose_name="NIT")
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.razon_social} ({self.nit})"


class ServicioContable(models.Model):
    """
    Asigna un servicio contable a una empresa y lo vincula a uno o varios empleados (Users).
    Solo usuarios que pertenezcan al grupo 'Empleado' deberían asignarse aquí.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="servicios_contables"
    )
    empleados = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="servicios_contables",
        help_text="Usuarios (empleados) asignados a llevar la contabilidad de esta empresa."
    )
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Servicio Contable"
        verbose_name_plural = "Servicios Contables"

    def __str__(self):
        return f"Servicio contable para {self.empresa.razon_social}"


# ------------------------------------------------------------
# 1. Plan de Cuentas (Chart of Accounts)
# ------------------------------------------------------------

class Cuenta(models.Model):
    """
    Representa una cuenta contable en el plan de cuentas.
    - código: Cadena jerárquica, ej. '1.01.05'
    - nombre: Nombre descriptivo de la cuenta.
    - tipo: Activo, Pasivo, Patrimonio, Ingreso, Gasto.
    - nivel: Nivel en la jerarquía (1, 2, 3, …).
    - cuenta_padre: Relación a sí misma para estructura jerárquica.
    """
    TIPO_CUENTA_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('PASIVO', 'Pasivo'),
        ('PATRIMONIO', 'Patrimonio'),
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES)
    nivel = models.PositiveIntegerField(default=1)
    cuenta_padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcuentas',
        null=True,
        blank=True
    )
   

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


# ------------------------------------------------------------
# 2. Mes (Periodo Contable)
# ------------------------------------------------------------

class Mes(models.Model):
    """
    Representa un período contable mensual para la empresa.
    Útil para agrupar asientos contables por mes.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='meses_contables'
    )
    ano = models.PositiveIntegerField()
    mes = models.PositiveIntegerField(
        choices=[(i, timezone.datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    )
    abierto = models.BooleanField(default=True)  # Si el mes está abierto para registros

    class Meta:
        verbose_name = "Mes Contable"
        verbose_name_plural = "Meses Contables"
        unique_together = ('empresa', 'ano', 'mes')
        ordering = ['ano', 'mes']

    def __str__(self):
        nombre_mes = timezone.datetime(2000, self.mes, 1).strftime('%B')
        return f"{nombre_mes} {self.ano} - {self.empresa.razon_social}"


# ------------------------------------------------------------
# 3. Libro Diario (Journal Entries) y Glosas
# ------------------------------------------------------------

class Glosa(models.Model):
    """
    Descripción o comentario que puede usarse comúnmente para asientos.
    """
    texto = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Glosa"
        verbose_name_plural = "Glosas"

    def __str__(self):
        return f"{self.texto}"


class AsientoDiario(models.Model):
    """
    Encabezado de un asiento en el Libro Diario.
    - fecha: Fecha del asiento.
    - glosa: Comentario general del asiento.
    - mes: Período contable al que pertenece.
    - numero_asiento: Consecutivo de asiento dentro del mes.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='asientos_diario'
    )
    mes = models.ForeignKey(
        Mes,
        on_delete=models.PROTECT,
        related_name='asientos_diario'
    )
    fecha = models.DateField()
    glosa = models.ForeignKey(
        Glosa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asientos'
    )
    numero_asiento = models.PositiveIntegerField(
        help_text="Consecutivo dentro del mes."
    )
    
    class Meta:
        verbose_name = "Asiento Diario"
        verbose_name_plural = "Asientos Diario"
        unique_together = ('mes', 'numero_asiento', 'empresa')
        ordering = ['mes__ano', 'mes__mes', 'numero_asiento']

    def __str__(self):
        return f"Asiento {self.numero_asiento} - {self.fecha} ({self.empresa.razon_social})"


class LineaAsiento(models.Model):
    """
    Detalle de cada línea de un AsientoDiario.
    - cuenta: Cuenta contable afectada.
    - debe o haber: Montos de débito/crédito.
    - descripción: Descripción específica (si se requiere detallar por línea).
    """
    asiento = models.ForeignKey(
        AsientoDiario,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,
        related_name='lineas_asiento'
    )
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Línea de Asiento"
        verbose_name_plural = "Líneas de Asiento"
        ordering = ['cuenta__codigo']

    def __str__(self):
        return f"{self.asiento} | {self.cuenta.codigo} | D: {self.debe} / H: {self.haber}"


# ------------------------------------------------------------
# 4. Libro Mayor (General Ledger)
# ------------------------------------------------------------

class LibroMayor(models.Model):
    """
    Encabezado del Libro Mayor para una empresa y un rango de fechas.
    Cada instancia agrupa todas las líneas de asiento de una cuenta
    para permitir el cálculo de saldos acumulados.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='libros_mayores'
    )
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,
        related_name='libros_mayores'
    )
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Libro Mayor"
        verbose_name_plural = "Libros Mayores"
        ordering = ['-fecha_fin', 'cuenta__codigo']

    def __str__(self):
        fin = self.fecha_fin or "hasta la fecha"
        return f"Mayor {self.cuenta.codigo} ({self.empresa.razon_social}) {self.fecha_inicio} - {fin}"


class LibroMayorLinea(models.Model):
    """
    Línea en el Libro Mayor: corresponde a cada movimiento
    (debe/haber) de un asiento diario para la cuenta asociada.
    Incluye el saldo acumulado tras aplicar este movimiento.
    """
    libro = models.ForeignKey(
        LibroMayor,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    asiento = models.ForeignKey(
        AsientoDiario,
        on_delete=models.CASCADE,
        related_name='lineas_mayor'
    )
    linea_asiento = models.ForeignKey(
        LineaAsiento,
        on_delete=models.PROTECT,
        related_name='lineas_mayor'
    )
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    saldo_acumulado = models.DecimalField(
        max_digits=14, 
        decimal_places=2, 
        default=0,
        help_text="Saldo de la cuenta tras este asiento"
    )

    class Meta:
        verbose_name = "Línea Libro Mayor"
        verbose_name_plural = "Líneas Libro Mayor"
        ordering = ['fecha', 'id']

    def __str__(self):
        return f"{self.fecha} | {self.cuenta.codigo} | D:{self.debe} H:{self.haber} S:{self.saldo_acumulado}"


# ------------------------------------------------------------
# 5. Balance General (Balance Sheet)
# ------------------------------------------------------------

class BalanceGeneral(models.Model):
    """
    Encabezado de un Balance General para una fecha determinada.
    Se agrupa por empresa y fecha de corte.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='balances_generales'
    )
    fecha_corte = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Balance General"
        verbose_name_plural = "Balances Generales"
        unique_together = ('empresa', 'fecha_corte')
        ordering = ['-fecha_corte']

    def __str__(self):
        return f"Balance al {self.fecha_corte} ({self.empresa.razon_social})"


class BalanceGeneralLinea(models.Model):
    """
    Detalle de cada línea del Balance General.
    Se vincula a una cuenta, y se guarda el monto que corresponde al corte.
    """
    balance = models.ForeignKey(
        BalanceGeneral,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,
        related_name='balance_lineas'
    )
    monto = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        verbose_name = "Línea Balance General"
        verbose_name_plural = "Líneas Balance General"
        ordering = ['cuenta__codigo']

    def __str__(self):
        return f"{self.balance.fecha_corte} | {self.cuenta.codigo} | {self.monto}"


# ------------------------------------------------------------
# 6. Otros Modelos Recomendados
# ------------------------------------------------------------

class PeriodoFiscal(models.Model):
    """
    Representa un año fiscal para la empresa. Podría usarse para agrupar meses o cierres anuales.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='periodos_fiscales'
    )
    ano = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Periodo Fiscal"
        verbose_name_plural = "Periodos Fiscales"
        unique_together = ('empresa', 'ano')
        ordering = ['-ano']

    def __str__(self):
        return f"{self.ano} ({self.empresa.razon_social})"


class AsientoAjuste(models.Model):
    """
    Asientos de ajuste para cierre de mes o año. 
    Se podría diferenciar por tipo (provisión, depreciación, ajuste de inventario, etc.).
    """
    TIPO_AJUSTE_CHOICES = [
        ('PROVISION', 'Provisión'),
        ('DEPRECIACION', 'Depreciación'),
        ('INVENTARIO', 'Inventario'),
        ('OTRO', 'Otro'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='asientos_ajuste'
    )
    periodo = models.ForeignKey(
        PeriodoFiscal,
        on_delete=models.PROTECT,
        related_name='asientos_ajuste'
    )
    tipo_ajuste = models.CharField(max_length=20, choices=TIPO_AJUSTE_CHOICES)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Asiento de Ajuste"
        verbose_name_plural = "Asientos de Ajuste"
        ordering = ['fecha']

    def __str__(self):
        return f"{self.get_tipo_ajuste_display()} - {self.fecha}"


class AsientoAjusteLinea(models.Model):
    """
    Detalle de cada línea de un asiento de ajuste.
    Similar a LíneaAsiento, pero específicamente para ajustes.
    """
    asiento_ajuste = models.ForeignKey(
        AsientoAjuste,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,
        related_name='lineas_ajuste'
    )
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Línea Asiento Ajuste"
        verbose_name_plural = "Líneas Asiento Ajuste"
        ordering = ['cuenta__codigo']

    def __str__(self):
        return f"{self.asiento_ajuste} | {self.cuenta.codigo} | D: {self.debe} / H: {self.haber}"


class CierreMensual(models.Model):
    """
    Registra el cierre contable mensual para una empresa:
    - periodo: Mes en el que se cierra
    - fecha_cierre: Fecha en que se realizó el cierre
    """
    mes = models.OneToOneField(
        Mes,
        on_delete=models.CASCADE,
        related_name='cierre'
    )
    fecha_cierre = models.DateField(default=timezone.now)
    cerrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cierres_mensuales'
    )

    class Meta:
        verbose_name = "Cierre Mensual"
        verbose_name_plural = "Cierres Mensuales"
        ordering = ['-fecha_cierre']

    def __str__(self):
        return f"Cierre {self.mes} por {self.cerrado_por}"


