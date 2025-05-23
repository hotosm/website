# Generated by Django 4.2.7 on 2024-09-23 17:43

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_newsownerpage_category_select_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsownerpage',
            name='view_all_news_url',
        ),
        migrations.AddField(
            model_name='newsownerpage',
            name='view_all_news_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
    ]
