# Generated by Django 4.2.7 on 2024-11-06 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_eventownerpage_applied_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventownerpage',
            name='date_date_text',
            field=models.CharField(default='date'),
        ),
        migrations.AddField(
            model_name='eventownerpage',
            name='date_from_text',
            field=models.CharField(default='From'),
        ),
        migrations.AddField(
            model_name='eventownerpage',
            name='date_to_text',
            field=models.CharField(default='To'),
        ),
    ]
