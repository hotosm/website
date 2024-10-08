# Generated by Django 4.2.7 on 2024-08-07 19:01

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('core', '0007_partnertype_partner_partner_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnertype',
            name='type_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='partnertype',
            name='type_icon',
            field=models.ForeignKey(help_text='Icon for the partner type', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
