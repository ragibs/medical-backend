# Generated by Django 5.1.2 on 2024-11-03 21:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedAppApi', '0002_testuser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicPatient',
            fields=[
                ('patient_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MedAppApi.patient')),
                ('maximum_appointments', models.IntegerField(default=100)),
            ],
            bases=('MedAppApi.patient',),
        ),
        migrations.CreateModel(
            name='ProPatient',
            fields=[
                ('patient_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MedAppApi.patient')),
                ('maximum_appointments', models.IntegerField(default=99999999)),
            ],
            bases=('MedAppApi.patient',),
        ),
        migrations.AddField(
            model_name='patient',
            name='appointments_booked',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='AdminStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimonial', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
