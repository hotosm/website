# Generated by Django 4.2.7 on 2024-07-08 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_page', '0002_searchpage_search_text_midfix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchpage',
            name='no_results_text',
            field=models.CharField(default='No matching search results for', help_text='This field is a prefix to the current search result in the event no results are found; i.e., if the search keyword was \'Hello\' and this field is \'No matching result for\', the no-result page would show "No matching result for "Hello""'),
        ),
    ]
