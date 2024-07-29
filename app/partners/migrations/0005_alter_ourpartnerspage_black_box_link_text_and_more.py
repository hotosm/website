# Generated by Django 4.2.7 on 2024-07-25 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0004_ourpartnerspage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourpartnerspage',
            name='black_box_link_text',
            field=models.CharField(default='Become a funder'),
        ),
        migrations.AlterField(
            model_name='ourpartnerspage',
            name='black_box_title',
            field=models.CharField(default='Become a funding partner'),
        ),
        migrations.AlterField(
            model_name='ourpartnerspage',
            name='red_box_link_text',
            field=models.CharField(default='Partner with us'),
        ),
        migrations.AlterField(
            model_name='ourpartnerspage',
            name='red_box_title',
            field=models.CharField(default='Learn ways to partner with HOT'),
        ),
    ]
