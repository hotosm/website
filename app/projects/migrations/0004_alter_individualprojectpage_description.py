# Generated by Django 4.2.7 on 2024-05-07 22:38

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_individualprojectpage_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualprojectpage',
            name='description',
            field=wagtail.fields.StreamField([('text_block', wagtail.blocks.RichTextBlock())], null=True, use_json_field=True),
        ),
    ]
