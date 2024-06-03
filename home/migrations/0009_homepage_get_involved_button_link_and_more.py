# Generated by Django 4.2.7 on 2024-05-27 23:44

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('home', '0008_blankinaccessiblepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='get_involved_button_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='get_involved_button_text',
            field=models.CharField(default='Get Involved'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='highlighted_programs',
            field=wagtail.fields.StreamField([('program', wagtail.blocks.PageChooserBlock(page_type=['programs.IndividualProgramPage']))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='highlighted_programs_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='highlighted_programs_title',
            field=models.CharField(default='Highlighted Programs'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='impact_areas_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='impact_areas_title',
            field=models.CharField(default='Impact Areas'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='mapping_hubs_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='mapping_hubs_title',
            field=wagtail.fields.RichTextField(blank=True, help_text='Any text written in bold will be displayed as red in this title.'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='opportunities_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='opportunities_title',
            field=wagtail.fields.RichTextField(blank=True, help_text='Any text written in bold will be displayed as red in this title.'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='our_work_title',
            field=models.CharField(default='Our Work'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_with_us_button_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_with_us_button_text',
            field=models.CharField(default='Partner With Us'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='tools_resources_button_text',
            field=models.CharField(default='Tools & Resources'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='tools_resources_button_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='tools_resources_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='tools_resources_image',
            field=models.ForeignKey(blank=True, help_text='Tools and Resources section image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='tools_resources_title',
            field=wagtail.fields.RichTextField(blank=True, help_text='Any text written in bold will be displayed as red in this title.'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='view_all_programs_text',
            field=models.CharField(default='View all programs'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='who_we_are_button_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='who_we_are_button_text',
            field=models.CharField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='who_we_are_intro_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='who_we_are_intro_title',
            field=wagtail.fields.RichTextField(blank=True, help_text='Any text written in bold will be displayed as red in this title.'),
        ),
    ]