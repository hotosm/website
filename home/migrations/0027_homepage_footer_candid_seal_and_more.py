# Generated by Django 4.2.7 on 2024-06-10 23:47

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('home', '0026_alter_homepage_navigation'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='footer_candid_seal',
            field=models.ForeignKey(blank=True, help_text='The Candid transparency seal image to be shown in the footer; this is shown on all pages.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='navigation',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('link_url', wagtail.blocks.URLBlock(help_text='A link URL or page must be provided; if both are present, the link will default to the page.', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(help_text='A link URL or page must be provided; if both are present, the link will default to the page.', required=False)), ('is_button', wagtail.blocks.BooleanBlock(help_text="Buttons will show as a red block with white text, show up last, and will show up on medium screens at all times. Buttons shouldn't have children.", required=False)), ('show_in_footer', wagtail.blocks.BooleanBlock(help_text="If checked, this item (and its children) will show in the footer's navigation; otherwise, it will not show up.", required=False)), ('children', wagtail.blocks.StreamBlock([('nav_item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('link_url', wagtail.blocks.URLBlock(help_text='A link URL or page must be provided; if both are present, the link will default to the pagee.', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(help_text='A link URL or page must be provided; if both are present, the link will default to the pagee.', required=False))]))], blank=True, null=True, required=False, use_json_field=True))]))], blank=True, help_text='The items of the navigation; this is shown on all pages.', null=True, use_json_field=True),
        ),
    ]
