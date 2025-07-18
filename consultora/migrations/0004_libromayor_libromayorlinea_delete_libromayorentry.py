# Generated by Django 5.2.3 on 2025-06-22 20:28

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultora', '0003_remove_cuenta_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibroMayor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='libros_mayores', to='consultora.cuenta')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libros_mayores', to='consultora.empresa')),
            ],
            options={
                'verbose_name': 'Libro Mayor',
                'verbose_name_plural': 'Libros Mayores',
                'ordering': ['-fecha_fin', 'cuenta__codigo'],
            },
        ),
        migrations.CreateModel(
            name='LibroMayorLinea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('debe', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('haber', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('saldo_acumulado', models.DecimalField(decimal_places=2, default=0, help_text='Saldo de la cuenta tras este asiento', max_digits=14)),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas_mayor', to='consultora.asientodiario')),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='consultora.libromayor')),
                ('linea_asiento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lineas_mayor', to='consultora.lineaasiento')),
            ],
            options={
                'verbose_name': 'Línea Libro Mayor',
                'verbose_name_plural': 'Líneas Libro Mayor',
                'ordering': ['fecha', 'id'],
            },
        ),
        migrations.DeleteModel(
            name='LibroMayorEntry',
        ),
    ]
