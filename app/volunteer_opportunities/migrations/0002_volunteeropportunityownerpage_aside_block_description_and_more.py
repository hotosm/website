# Generated by Django 4.2.7 on 2024-07-16 16:52

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('volunteer_opportunities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='aside_block_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='aside_block_link_text',
            field=models.CharField(default='Contact us'),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='aside_block_link_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='aside_block_title',
            field=models.CharField(default="Didn't find the volunteer opportunity you were looking for?"),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='black_box_link_text',
            field=models.CharField(default='See our events'),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='black_box_link_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='black_box_title',
            field=models.CharField(default='Check out upcoming events'),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='body_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='header_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='Header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='open_opportunities_title',
            field=models.CharField(default='Open Opportunities'),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='red_box_link_text',
            field=models.CharField(default='Join our conversation'),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='red_box_link_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='volunteeropportunityownerpage',
            name='red_box_title',
            field=models.CharField(default='Join our Slack channel and find more opportunities'),
        ),
    ]