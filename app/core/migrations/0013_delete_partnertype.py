# Generated by Django 4.2.7 on 2024-08-14 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_partner_partner_type_partner_partner_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PartnerType',
        ),
    ]
