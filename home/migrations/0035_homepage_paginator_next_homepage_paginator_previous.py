# Generated by Django 4.2.7 on 2024-09-11 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_alter_homepage_carousel_alter_homepage_e404_links_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='paginator_next',
            field=models.CharField(default='Next'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='paginator_previous',
            field=models.CharField(default='Previous'),
        ),
    ]