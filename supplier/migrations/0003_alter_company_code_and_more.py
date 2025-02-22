# Generated by Django 5.1.5 on 2025-02-01 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_alter_supplier_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='code',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='compliance_threshhold',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compliance_thresholds', to='supplier.supplier'),
        ),
    ]
