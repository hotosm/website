# Generated by Django 4.2.7 on 2024-07-29 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0006_dataprinciplespage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataprinciplespage',
            name='footer_button_text',
            field=models.CharField(default='View the Principles as a Presentation'),
        ),
    ]
