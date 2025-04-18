# Generated by Django 4.2.7 on 2024-10-10 17:41

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0006_alter_techproductsuitepage_product_suite_learn_more_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualtechstackpage',
            name='link_blocks',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('linktext', wagtail.blocks.CharBlock()), ('linkurl', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))]))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='black_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='go_back_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='red_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='tech_stack_cta_button_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
    ]
