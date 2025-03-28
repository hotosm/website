# Generated by Django 4.2.7 on 2025-03-24 22:34

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0055_alter_individualprojectpage_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualprojectpage',
            name='tools_list',
            field=wagtail.fields.StreamField([('tool', 0), ('manual_tool', 3)], blank=True, block_lookup={0: ('wagtail.blocks.PageChooserBlock', (), {'page_type': ['tech.IndividualTechStackPage']}), 1: ('wagtail.blocks.CharBlock', (), {}), 2: ('wagtail.blocks.URLBlock', (), {'required': False}), 3: ('wagtail.blocks.StructBlock', [[('text', 1), ('link', 2)]], {})}, null=True),
        ),
    ]
