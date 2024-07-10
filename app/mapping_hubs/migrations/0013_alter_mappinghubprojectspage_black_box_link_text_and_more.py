# Generated by Django 4.2.7 on 2024-07-04 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapping_hubs', '0012_mappinghubprojectspage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappinghubprojectspage',
            name='black_box_link_text',
            field=models.CharField(default='Get involved'),
        ),
        migrations.AlterField(
            model_name='mappinghubprojectspage',
            name='black_box_title',
            field=models.CharField(default='See the many ways to get involved with HOT and open mapping'),
        ),
        migrations.AlterField(
            model_name='mappinghubprojectspage',
            name='red_box_link_text',
            field=models.CharField(default='Explore projects'),
        ),
        migrations.AlterField(
            model_name='mappinghubprojectspage',
            name='red_box_title',
            field=models.CharField(default="See all of HOT's projects"),
        ),
    ]