# Generated by Django 4.2.7 on 2024-05-13 19:52

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_rename_call_to_action_link_individualprojectpage_call_to_action_link_text_and_more'),
        ('news', '0007_alter_newscategory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualnewspage',
            name='related_projects',
            field=modelcluster.fields.ParentalManyToManyField(to='projects.individualprojectpage'),
        ),
    ]
