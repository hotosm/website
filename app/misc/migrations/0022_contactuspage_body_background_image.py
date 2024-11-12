# Generated by Django 4.2.7 on 2024-09-10 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('misc', '0021_alter_codeofconductpage_our_policies_links_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactuspage',
            name='body_background_image',
            field=models.ForeignKey(blank=True, help_text='Shows behind the entire body', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
