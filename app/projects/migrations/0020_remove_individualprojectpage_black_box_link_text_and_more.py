# Generated by Django 4.2.7 on 2024-06-04 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_projectownerpage_view_all_events_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='black_box_link_text',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='black_box_link_url',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='black_box_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='contact_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='duration_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='impact_areas_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='partners_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='red_box_link_text',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='red_box_link_url',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='red_box_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='region_hub_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='related_events_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='related_news_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='tools_title',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='view_all_events_text',
        ),
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='view_all_news_text',
        ),
    ]