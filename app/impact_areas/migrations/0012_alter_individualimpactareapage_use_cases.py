# Generated by Django 4.2.7 on 2024-05-23 20:38

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('impact_areas', '0011_individualimpactareapage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualimpactareapage',
            name='use_cases',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('description', wagtail.blocks.RichTextBlock()), ('link_text', wagtail.blocks.CharBlock()), ('link_url', wagtail.blocks.URLBlock(blank=True, null=True))]))], blank=True, null=True, use_json_field=True),
        ),
    ]
