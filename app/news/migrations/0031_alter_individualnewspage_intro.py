# Generated by Django 4.2.7 on 2025-03-26 19:18

from django.db import migrations
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0030_newsownerpage_fallback_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualnewspage',
            name='intro',
            field=wagtailmarkdown.fields.MarkdownField(blank=True),
        ),
    ]
