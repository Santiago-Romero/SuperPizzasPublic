# Generated by Django 2.2.5 on 2019-10-07 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('franquicias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipofranquicia',
            name='precio',
            field=models.IntegerField(default=0),
        ),
    ]
