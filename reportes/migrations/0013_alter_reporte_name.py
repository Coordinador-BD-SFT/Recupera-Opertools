# Generated by Django 5.1.1 on 2024-09-16 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0012_alter_reporte_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]