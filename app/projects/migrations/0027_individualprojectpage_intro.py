# Generated by Django 4.2.7 on 2024-07-08 21:32

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0026_remove_individualprojectpage_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprojectpage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
