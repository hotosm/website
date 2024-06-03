# Generated by Django 4.2.7 on 2024-05-13 21:51

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_individualnewspage_related_news_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualnewspage',
            name='test_thing',
            field=wagtail.fields.StreamField([('project_page', wagtail.blocks.PageChooserBlock(page_type=['projects.IndividualProjectPage']))], blank=True, null=True, use_json_field=True),
        ),
    ]