# Generated by Django 4.2.7 on 2024-10-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0022_individualnewspage_associated_hubs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsownerpage',
            name='filter_by_hub',
            field=models.CharField(default='Filter by Hub'),
        ),
    ]
