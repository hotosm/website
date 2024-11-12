# Generated by Django 4.2.7 on 2024-11-05 22:47

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('impact_areas', '0023_individualimpactareapage_description_extended_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualimpactareapage',
            name='use_cases',
            field=wagtail.fields.StreamField([('blocks', 7)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {}), 1: ('wagtail.blocks.RichTextBlock', (), {}), 2: ('wagtail.blocks.PageChooserBlock', (), {}), 3: ('wagtail.blocks.URLBlock', (), {}), 4: ('wagtail.documents.blocks.DocumentChooserBlock', (), {}), 5: ('wagtail.blocks.CharBlock', (), {'help_text': "Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."}), 6: ('wagtail.blocks.StreamBlock', [[('page', 2), ('url', 3), ('document', 4), ('other', 5)]], {'blank': True, 'null': True}), 7: ('wagtail.blocks.StructBlock', [[('title', 0), ('description', 1), ('link_text', 0), ('link', 6)]], {})}, null=True),
        ),
    ]