# Generated by Django 4.2.7 on 2024-05-14 16:44

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('news', '0012_individualnewspage_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='news.individualnewspage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='individualnewspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='news.NewsTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
