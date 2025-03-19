# Generated by Django 5.1.7 on 2025-03-18 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('profile_picture_url', models.URLField(blank=True, null=True)),
                ('doctor_name', models.CharField(blank=True, max_length=255, null=True)),
                ('clinic_name', models.CharField(blank=True, max_length=255, null=True)),
                ('appointment_date', models.DateField(blank=True, null=True)),
                ('appointment_time', models.TimeField(blank=True, null=True)),
                ('appointment_type', models.CharField(blank=True, max_length=255, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('applicant_username', models.CharField(blank=True, max_length=255, null=True)),
                ('applicant_first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('applicant_last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
