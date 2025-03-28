# Generated by Django 4.2.7 on 2024-09-16 19:37

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('who_we_are', '0006_alter_whowearepage_black_box_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whowearepage',
            name='other_page_preview_blocks',
            field=wagtail.fields.StreamField([('other_page_preview', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('description', wagtail.blocks.RichTextBlock(required=False)), ('page', wagtail.blocks.PageChooserBlock())]))], blank=True, null=True, use_json_field=True),
        ),
    ]
