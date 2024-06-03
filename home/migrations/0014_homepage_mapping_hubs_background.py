# Generated by Django 4.2.7 on 2024-05-29 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('home', '0013_homepage_our_work_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='mapping_hubs_background',
            field=models.ForeignKey(blank=True, help_text='The background that shows in the default info panel for Open Mapping Hubs', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]