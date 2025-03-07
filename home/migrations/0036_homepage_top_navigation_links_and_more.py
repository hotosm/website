# Generated by Django 4.2.7 on 2024-09-16 21:37

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_homepage_paginator_next_homepage_paginator_previous'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='top_navigation_links',
            field=wagtail.fields.StreamField([('link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], required=False))]))], blank=True, help_text='Links to be shown in the topmost navigation bar.', null=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='top_navigation_socials',
            field=wagtail.fields.StreamField([('social', wagtail.blocks.StructBlock([('service', wagtail.blocks.CharBlock()), ('icon', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], required=False))]))], blank=True, help_text='Social media links to be shown in the topmost navigation bar.', null=True, use_json_field=True),
        ),
    ]
