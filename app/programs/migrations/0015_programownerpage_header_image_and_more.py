# Generated by Django 4.2.7 on 2024-11-04 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0026_delete_uploadedimage'),
        ('programs', '0014_individualprogrampage_program_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='programownerpage',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='Header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='keyword_search_hint',
            field=models.CharField(default='Search by keyword'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='remove_filters_text',
            field=models.CharField(default='Reset Filters'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='search_button_text',
            field=models.CharField(default='Apply Filters'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='sort_by_new',
            field=models.CharField(default='Sort by New'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='sort_by_old',
            field=models.CharField(default='Sort by Old'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='sort_by_titlea',
            field=models.CharField(default='Sort by Title Alphabetical'),
        ),
        migrations.AddField(
            model_name='programownerpage',
            name='sort_by_titlez',
            field=models.CharField(default='Sort by Title Reverse Alphabetical'),
        ),
    ]
