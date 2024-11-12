# Generated by Django 4.2.7 on 2024-10-03 19:14

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_homepage_home_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='home_stats',
            field=wagtail.fields.StreamField([('stat', wagtail.blocks.StructBlock([('fallback_number', wagtail.blocks.CharBlock(help_text='Displays if no API is given, or if the API call fails.')), ('statistic', wagtail.blocks.CharBlock()), ('tooltip', wagtail.blocks.CharBlock(help_text="If this field is filled, an info 'i' will appear in this stat block, which will show this text when hovered.", required=False)), ('api', wagtail.blocks.StreamBlock([('api', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(help_text='This name will be used for caching the result of this API, and as such, should be unique.')), ('endpoint', wagtail.blocks.CharBlock(help_text='This is the URL that will be called; should return a JSON object.')), ('key_path', wagtail.blocks.StreamBlock([('key', wagtail.blocks.CharBlock())], help_text="This should lead to the value that should be displayed for this API; i.e., if the result of calling the endpoint is a JSON object { 'result': {'stat': 10 } }, this field should have 'result' and 'stat' as keys, in that order, so as to navigate to ['result']['stat']."))]))], help_text='', required=False))]))], blank=True, help_text='Do not touch this field unless you know what you are doing.', use_json_field=True),
        ),
    ]