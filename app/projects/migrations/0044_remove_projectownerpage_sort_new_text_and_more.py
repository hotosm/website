# Generated by Django 4.2.7 on 2024-11-06 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0043_projectownerpage_apply_filter_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectownerpage',
            name='sort_new_text',
        ),
        migrations.RemoveField(
            model_name='projectownerpage',
            name='sort_old_text',
        ),
    ]