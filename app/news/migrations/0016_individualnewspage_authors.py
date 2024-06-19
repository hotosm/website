# Generated by Django 4.2.7 on 2024-06-04 16:57

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_alter_individualnewspage_article_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualnewspage',
            name='authors',
            field=wagtail.fields.StreamField([('author', wagtail.blocks.PageChooserBlock(page_type=['members.IndividualMemberPage']))], blank=True, null=True, use_json_field=True),
        ),
    ]