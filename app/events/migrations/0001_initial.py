# Generated by Django 4.2.7 on 2024-06-05 19:43

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOwnerPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('event_location_title', models.CharField(default='Event Location')),
                ('join_event_title', models.CharField(default='Join This Event')),
                ('rsvp_button_text', models.CharField(default='RSVP')),
                ('more_events_title', models.CharField(default='More Events')),
                ('view_all_events_text', models.CharField(default='View all Events')),
                ('view_all_events_url', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='IndividualEventPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('extended_description', wagtail.fields.StreamField([('text_block', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote']))], null=True, use_json_field=True)),
                ('event_location', models.CharField(blank=True)),
                ('rsvp_description', wagtail.fields.RichTextField(blank=True)),
                ('rsvp_link', models.URLField(blank=True)),
                ('image', models.ForeignKey(blank=True, help_text='Image to represent the event', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
