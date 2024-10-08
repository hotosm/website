# Generated by Django 4.2.7 on 2024-09-03 21:39

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0003_techproductsuitepage_product_suite_learn_more_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualtechstackpage',
            name='link_blocks',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('linktext', wagtail.blocks.CharBlock()), ('linkurl', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())]))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='black_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='go_back_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='red_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='techproductsuitepage',
            name='tech_stack_cta_button_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], blank=True, use_json_field=True),
        ),
    ]
