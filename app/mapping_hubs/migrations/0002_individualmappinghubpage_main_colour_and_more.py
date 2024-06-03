# Generated by Django 4.2.7 on 2024-05-21 21:50

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('mapping_hubs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualmappinghubpage',
            name='main_colour',
            field=models.CharField(default='#FFFFFF', help_text='The main colour for this mapping hub. This should be a hex code (though any type of CSS colour format will work).'),
        ),
        migrations.AddField(
            model_name='individualmappinghubpage',
            name='main_external_hub_image',
            field=models.ForeignKey(blank=True, help_text='A larger image that represents this hub which may be shown on other pages', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='individualmappinghubpage',
            name='main_icon',
            field=models.ForeignKey(blank=True, help_text='The main icon that should show for this page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='contact_section_links',
            field=wagtail.fields.StreamField([('contact_link', wagtail.blocks.StreamBlock([('blocks', wagtail.blocks.StructBlock([('link_text', wagtail.blocks.CharBlock(required=True)), ('link_url', wagtail.blocks.URLBlock(blank=True, required=False))]))]))], blank=True, use_json_field=True),
        ),
    ]