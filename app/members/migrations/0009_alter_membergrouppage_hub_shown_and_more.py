# Generated by Django 4.2.7 on 2024-07-09 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_membergrouppage_hub_shown_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membergrouppage',
            name='hub_shown',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='membergrouppage',
            name='position_shown',
            field=models.BooleanField(default=False),
        ),
    ]
