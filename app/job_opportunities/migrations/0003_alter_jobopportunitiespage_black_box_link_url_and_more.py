# Generated by Django 4.2.7 on 2024-10-10 17:41

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job_opportunities', '0002_jobopportunitiespage_black_box_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobopportunitiespage',
            name='black_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='jobopportunitiespage',
            name='red_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='jobopportunitiespage',
            name='rfp_banner_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
    ]
