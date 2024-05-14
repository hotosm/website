# Generated by Django 4.2.7 on 2024-05-13 19:15

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_newscategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newscategory',
            options={'verbose_name_plural': 'News Categories'},
        ),
        migrations.AddField(
            model_name='individualnewspage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='news.newscategory'),
        ),
    ]
