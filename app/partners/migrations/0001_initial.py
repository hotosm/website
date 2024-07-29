# Generated by Django 4.2.7 on 2024-07-25 18:00

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerWithUsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('header_description', wagtail.fields.RichTextField(blank=True)),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('partnership_types_title', models.CharField(default='Types of Partnerships')),
                ('partnership_types', wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('icon', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock())]))], blank=True, help_text='Blocks to be shown under the Types of Partnerships section.', null=True, use_json_field=True)),
                ('meet_our_partners_title', models.CharField(default='Meet Our Partners')),
                ('view_all_partners_text', models.CharField(default='View All Partners')),
                ('view_all_partners_link', wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True)),
                ('red_box_title', models.CharField(default='Still have questions?')),
                ('red_box_link_text', models.CharField(default='Contact our team')),
                ('red_box_link_url', wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True)),
                ('black_box_title', models.CharField(default='Become a Partner')),
                ('black_box_link_text', models.CharField(default='Email to partnerships@hotosm.org')),
                ('black_box_link_url', wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='Header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
