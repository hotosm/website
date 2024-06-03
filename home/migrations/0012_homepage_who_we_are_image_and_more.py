# Generated by Django 4.2.7 on 2024-05-28 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('home', '0011_rename_related_news_homepage_displayed_news_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='who_we_are_image',
            field=models.ForeignKey(blank=True, help_text='Who we are image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='who_we_are_button_text',
            field=models.CharField(default='Who We Are'),
        ),
    ]
