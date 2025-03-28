# Generated by Django 4.2.7 on 2024-10-10 17:41

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rfp', '0007_rename_header_description_requestforproposalownerpage_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestforproposalownerpage',
            name='job_opportunities_button_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
    ]
