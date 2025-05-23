# Generated by Django 4.2.7 on 2024-09-18 19:59

from django.db import migrations, models
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_eventownerpage_category_select_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventownerpage',
            name='view_all_events_url',
        ),
        migrations.AddField(
            model_name='eventownerpage',
            name='view_all_events_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='individualeventpage',
            name='end_date_time',
            field=models.DateTimeField(help_text='This datetime is in UTC.'),
        ),
        migrations.AlterField(
            model_name='individualeventpage',
            name='start_date_time',
            field=models.DateTimeField(help_text='This datetime is in UTC.'),
        ),
    ]
