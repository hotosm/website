# Generated by Django 4.2.7 on 2024-11-05 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0018_individualprogrampage_stat_section_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprogrampage',
            name='bigger_intro',
        ),
    ]