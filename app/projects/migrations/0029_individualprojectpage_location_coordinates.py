# Generated by Django 4.2.7 on 2024-08-07 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_projecttype_individualprojectpage_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprojectpage',
            name='location_coordinates',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
