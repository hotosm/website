# Generated by Django 4.2.7 on 2024-06-27 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_projectownerpage_load_more_projects_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='owner_region_hub',
        ),
    ]
