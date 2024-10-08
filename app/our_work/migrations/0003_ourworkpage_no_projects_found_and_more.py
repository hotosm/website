# Generated by Django 4.2.7 on 2024-08-12 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_work', '0002_remove_ourworkpage_f_project_active_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ourworkpage',
            name='no_projects_found',
            field=models.CharField(default='No projects found with the applied filters.'),
        ),
        migrations.AlterField(
            model_name='ourworkpage',
            name='black_box_link_text',
            field=models.CharField(default='Get Involved with HOT'),
        ),
        migrations.AlterField(
            model_name='ourworkpage',
            name='black_box_title',
            field=models.CharField(default='Check many opportunities to get involved with HOT!'),
        ),
        migrations.AlterField(
            model_name='ourworkpage',
            name='red_box_link_text',
            field=models.CharField(default='View all events'),
        ),
        migrations.AlterField(
            model_name='ourworkpage',
            name='red_box_title',
            field=models.CharField(default='Check our upcoming events!'),
        ),
    ]
