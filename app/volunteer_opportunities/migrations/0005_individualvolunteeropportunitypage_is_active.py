# Generated by Django 4.2.7 on 2024-07-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer_opportunities', '0004_volunteeropportunityownerpage_no_opportunities_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualvolunteeropportunitypage',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
