# Generated by Django 4.2.7 on 2024-11-04 23:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0013_alter_programownerpage_bottom_banner_link_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprogrampage',
            name='program_start_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='This is not shown on the program page itself, and is basically just used for sorting on the program owner page.'),
            preserve_default=False,
        ),
    ]
