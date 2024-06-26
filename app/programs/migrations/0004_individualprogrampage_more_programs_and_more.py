# Generated by Django 4.2.7 on 2024-05-15 23:33

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0003_individualprogrampage_view_all_partners_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprogrampage',
            name='more_programs',
            field=wagtail.fields.StreamField([('program_page', wagtail.blocks.PageChooserBlock(page_type=['programs.IndividualProgramPage']))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='individualprogrampage',
            name='view_all_partners_link',
            field=models.CharField(blank=True),
        ),
        migrations.AddField(
            model_name='individualprogrampage',
            name='view_all_programs_link',
            field=models.URLField(blank=True),
        ),
    ]
