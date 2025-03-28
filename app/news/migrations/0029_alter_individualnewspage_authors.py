# Generated by Django 4.2.7 on 2025-03-17 23:30

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0028_remove_individualnewspage_test_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualnewspage',
            name='authors',
            field=wagtail.fields.StreamField([('author', 0), ('manual_author', 1)], blank=True, block_lookup={0: ('wagtail.blocks.PageChooserBlock', (), {'page_type': ['members.IndividualMemberPage']}), 1: ('wagtail.blocks.CharBlock', (), {})}, null=True),
        ),
    ]
