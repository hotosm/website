# Generated by Django 4.2.7 on 2024-08-08 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_individualprojectpage_location_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprojectpage',
            name='project_active',
            field=models.BooleanField(default=True),
        ),
    ]
