# Generated by Django 4.2.7 on 2024-10-01 19:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('misc', '0027_donatepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatepage',
            name='banner_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='donatepage',
            name='banner_image',
            field=models.ForeignKey(blank=True, help_text='Header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='donatepage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='donatepage',
            name='other_ways_to_donate',
            field=wagtail.fields.StreamField([('icon', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='donatepage',
            name='other_ways_to_donate_title',
            field=models.CharField(default='Other Ways to Donate'),
        ),
    ]