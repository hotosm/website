# Generated by Django 4.2.7 on 2024-05-15 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('projects', '0008_individualprojectpage_related_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprojectpage',
            name='program',
        ),
        migrations.AddField(
            model_name='individualprojectpage',
            name='owner_program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page'),
        ),
    ]
