# Generated by Django 4.2.7 on 2024-05-23 17:22

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapping_hubs', '0007_individualmappinghubpage_dogear_boxes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='dogear_boxes',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('link_text', wagtail.blocks.CharBlock(required=True)), ('link_url', wagtail.blocks.URLBlock(blank=True, required=False))]))], blank=True, help_text="These are, for example, the 'Grants' and 'Map and Chat Hour' boxes in the Asia-Pacific page. Please only add these in pairs of 2!", use_json_field=True),
        ),
    ]
