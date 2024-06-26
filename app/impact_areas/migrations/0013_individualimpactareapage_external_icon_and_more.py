# Generated by Django 4.2.7 on 2024-05-23 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('impact_areas', '0012_alter_individualimpactareapage_use_cases'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualimpactareapage',
            name='external_icon',
            field=models.ForeignKey(blank=True, help_text='The icon representing this page which is shown for previews of this page on other pages.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='individualimpactareapage',
            name='load_more_projects_text',
            field=models.CharField(default='Load More Projects'),
        ),
    ]
