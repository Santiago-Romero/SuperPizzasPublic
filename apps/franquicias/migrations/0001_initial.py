
from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoFranquicia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Franquicia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_corte', models.DateField(auto_now_add=True)),
                ('configuracion', models.CharField(default='{"colorprimario":"#1D1D1D","colorsecundario":"#E9951F", "tamanioletra":100}', max_length=200)),
                ('media', models.FileField(blank=True, default='media/logos-franquicias/1_logo_default.png', null=True, upload_to='media/logos-franquicias/')),
                ('working', models.BooleanField(default=True)),
                ('tipo', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='franquicias.TipoFranquicia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dominio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='franquicias.Franquicia')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
