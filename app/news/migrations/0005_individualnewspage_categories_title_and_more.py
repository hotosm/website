# Generated by Django 4.2.7 on 2024-05-13 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_individualnewspage_related_news_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualnewspage',
            name='categories_title',
            field=models.CharField(default='Categories'),
        ),
        migrations.AddField(
            model_name='individualnewspage',
            name='tags_title',
            field=models.CharField(default='Tags'),
        ),
    ]
