# Generated by Django 4.2.7 on 2025-03-21 22:22

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0051_projectownerpage_duration_ongoing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprojectpage',
            name='is_community_led',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='individualprojectpage',
            name='country_text',
            field=wagtail.fields.RichTextField(blank=True, help_text='This field is mostly for projects with no specified region hub. Regardless, if region hub(s) and country are both provided, both fields will appear on the page.'),
        ),
    ]
