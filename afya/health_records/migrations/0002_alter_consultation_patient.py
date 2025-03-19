# Generated by Django 5.1.7 on 2025-03-19 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_consultations', to='health_records.patient'),
        ),
    ]
