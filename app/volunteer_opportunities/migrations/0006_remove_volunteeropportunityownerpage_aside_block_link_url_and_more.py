# Generated by Django 4.2.7 on 2024-09-13 18:02

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer_opportunities', '0005_individualvolunteeropportunitypage_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteeropportunityownerpage',
            name='aside_block_link_url',
        ),
        migrations.RemoveField(
            model_name='volunteeropportunityownerpage',
            name='black_box_link_url',
        ),
        migrations.RemoveField(
            model_name='volunteeropportunityownerpage',
            name='red_box_link_url',
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='aside_block_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='black_box_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='red_box_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
    ]
