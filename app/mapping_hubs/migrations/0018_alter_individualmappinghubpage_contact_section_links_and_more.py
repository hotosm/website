# Generated by Django 4.2.7 on 2024-09-03 21:39

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapping_hubs', '0017_individualmappinghubpage_external_description_long'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='contact_section_links',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('link_text', wagtail.blocks.CharBlock(required=True)), ('link_url', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, required=False))]))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='dogear_boxes',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(required=True)), ('link_url', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, required=False))]))], blank=True, help_text="These are, for example, the 'Grants' and 'Map and Chat Hour' boxes in the Asia-Pacific page. Please only add these in pairs of 2!", use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='events_section_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='header_project_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='news_section_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='project_section_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualmappinghubpage',
            name='subscribe_box_signup_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='mappinghubprojectspage',
            name='black_box_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='mappinghubprojectspage',
            name='red_box_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='openmappinghubspage',
            name='header_events_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='openmappinghubspage',
            name='header_news_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='openmappinghubspage',
            name='partners_section_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
    ]
