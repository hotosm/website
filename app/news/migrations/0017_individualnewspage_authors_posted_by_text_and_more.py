# Generated by Django 4.2.7 on 2024-06-04 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_individualnewspage_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualnewspage',
            name='authors_posted_by_text',
            field=models.CharField(default='Posted by', help_text="The text which appears prior to the authors names; with 'posted by', the text displays as 'posted by [author]'."),
        ),
        migrations.AddField(
            model_name='individualnewspage',
            name='authors_posted_on_text',
            field=models.CharField(default='on', help_text="The text which appears prior to the date; with 'on', it would display as 'on [date]'."),
        ),
    ]
