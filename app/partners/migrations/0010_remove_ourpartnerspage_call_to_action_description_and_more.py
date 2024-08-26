# Generated by Django 4.2.7 on 2024-08-13 23:17

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0009_partnershiptemplatepage_external_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='call_to_action_description',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='call_to_action_link_text',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='call_to_action_link_url',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='call_to_action_title',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='meet_partners_title',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='related_news_title',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='related_projects_title',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='view_partners_link',
        ),
        migrations.RemoveField(
            model_name='ourpartnerspage',
            name='view_partners_text',
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='call_to_action_description',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='call_to_action_link_text',
            field=models.CharField(default='Call to Action Link'),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='call_to_action_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='call_to_action_title',
            field=models.CharField(default='Call to Action'),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='meet_partners_title',
            field=models.CharField(default='Meet Our Partners'),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='related_news_title',
            field=models.CharField(default='Related News'),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='related_projects_title',
            field=models.CharField(default='Related Projects'),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='view_partners_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='partnerwithuspage',
            name='view_partners_text',
            field=models.CharField(default='View All Partners'),
        ),
    ]
