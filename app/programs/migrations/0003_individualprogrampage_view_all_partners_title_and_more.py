# Generated by Django 4.2.7 on 2024-05-15 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_individualprogrampage_partners'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprogrampage',
            name='view_all_partners_title',
            field=models.CharField(default='View All Partners'),
        ),
        migrations.AddField(
            model_name='individualprogrampage',
            name='view_all_programs_title',
            field=models.CharField(default='View All Programs'),
        ),
    ]
