# Generated by Django 4.2.7 on 2025-03-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0054_alter_individualprojectpage_project_contributors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualprojectpage',
            name='location',
            field=models.CharField(blank=True, help_text='This location will appear in the header if provided.'),
        ),
    ]
