# Generated by Django 4.2.7 on 2024-07-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_membergroupownerpage_view_all_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membergroupownerpage',
            name='sort_by_titlea',
            field=models.CharField(default='Sort by Name Alphabetical'),
        ),
        migrations.AlterField(
            model_name='membergroupownerpage',
            name='sort_by_titlez',
            field=models.CharField(default='Sort by Name Reverse Alphabetical'),
        ),
    ]
