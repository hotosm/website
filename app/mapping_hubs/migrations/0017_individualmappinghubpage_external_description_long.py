# Generated by Django 4.2.7 on 2024-08-02 21:48

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapping_hubs', '0016_alter_individualmappinghubpage_dogear_boxes'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualmappinghubpage',
            name='external_description_long',
            field=wagtail.fields.RichTextField(blank=True, help_text='A long description of the page to be used in external pages, such as the Open Mapping Hubs page.'),
        ),
    ]