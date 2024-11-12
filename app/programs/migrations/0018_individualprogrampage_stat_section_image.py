# Generated by Django 4.2.7 on 2024-11-05 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0026_delete_uploadedimage'),
        ('programs', '0017_individualprogrampage_bigger_intro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprogrampage',
            name='stat_section_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
