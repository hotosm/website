# Generated by Django 4.2.7 on 2024-05-07 16:12

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('impact_areas', '0008_alter_impactareaspage_impact_area_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactareaspage',
            name='impact_area_blocks',
            field=wagtail.fields.StreamField([('impact_area_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('link', wagtail.blocks.URLBlock(null=True))]))], null=True, use_json_field=True),
        ),
    ]
