# Generated by Django 4.2.7 on 2024-11-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_eventownerpage_date_date_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventownerpage',
            name='date_date_text',
            field=models.CharField(default='Filter by Date'),
        ),
    ]
