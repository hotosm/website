# Generated by Django 4.2.7 on 2024-07-17 22:42

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0004_joinourconversationpage_code_of_conduct_link_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='joinourconversationpage',
            name='black_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='joinourconversationpage',
            name='red_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True),
        ),
    ]
