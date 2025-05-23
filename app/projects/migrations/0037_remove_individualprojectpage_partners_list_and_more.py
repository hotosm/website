# Generated by Django 4.2.7 on 2024-09-18 22:14

import app.core.models
from django.db import migrations
import wagtail.fields
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_remove_individualprojectpage_call_to_action_link_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='partners_list',
        ),
        migrations.AddField(
            model_name='individualprojectpage',
            name='partner_list',
            field=wagtail.fields.StreamField([('partner', wagtail.snippets.blocks.SnippetChooserBlock(app.core.models.Partner))], blank=True, null=True, use_json_field=True),
        ),
    ]
