# Generated by Django 4.2.7 on 2024-05-21 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0005_individualprogrampage_bottom_banner_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualprogrampage',
            name='bottom_banner_text',
            field=models.CharField(default='Check out many opportunities to get involved with HOT!'),
        ),
    ]
