# Generated by Django 4.2.7 on 2024-09-25 21:52

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_alter_membergroupownerpage_sort_by_titlea_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membergroupownerpage',
            name='footer_box_button_link',
        ),
        migrations.AddField(
            model_name='membergroupownerpage',
            name='footer_box_button_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
    ]
