# Generated by Django 5.1.2 on 2024-11-04 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedAppApi', '0004_appointment_cost_satisfactionratings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SatisfactionRatings',
            new_name='Ratings',
        ),
    ]