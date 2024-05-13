# Generated by Django 4.2.7 on 2024-05-13 21:21

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_rename_call_to_action_link_individualprojectpage_call_to_action_link_text_and_more'),
        ('news', '0008_individualnewspage_related_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualnewspage',
            name='related_news',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='news.individualnewspage'),
        ),
        migrations.AlterField(
            model_name='individualnewspage',
            name='related_projects',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='projects.individualprojectpage'),
        ),
    ]
