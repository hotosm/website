# Generated by Django 4.2.7 on 2024-07-08 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_projectownerpage_header_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='intro',
        ),
    ]