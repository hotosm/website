# Generated by Django 4.2.7 on 2024-07-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventownerpage_event_categories_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventhosttype',
            options={'verbose_name_plural': 'Event Host Types'},
        ),
        migrations.AddField(
            model_name='eventownerpage',
            name='category_select',
            field=models.CharField(default='Filter by category'),
        ),
        migrations.AddField(
            model_name='eventownerpage',
            name='filter_by_country',
            field=models.CharField(default='Filter by country'),
        ),
        migrations.AddField(
            model_name='eventownerpage',
            name='host_type_select',
            field=models.CharField(default='Filter by host type'),
        ),
    ]
