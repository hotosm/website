# Generated by Django 4.2.7 on 2024-09-16 22:40

from django.db import migrations, models
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_homepage_top_navigation_links_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='top_navigation_donate_text',
            field=models.CharField(default='Donate'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='top_navigation_donate_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
    ]