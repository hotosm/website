# Generated by Django 4.2.7 on 2024-10-21 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0026_delete_uploadedimage'),
        ('mapping_hubs', '0021_alter_individualmappinghubpage_contact_section_links_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualmappinghubpage',
            name='hub_portrait_image',
            field=models.ForeignKey(blank=True, help_text="The image which shows for this hub on the home page in the 'Open Mapping Hubs' section in large screen sizes. This image should be more of a portrait, centered on what you want to be shown.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
