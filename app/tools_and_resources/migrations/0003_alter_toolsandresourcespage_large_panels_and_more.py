# Generated by Django 4.2.7 on 2024-08-15 19:35

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('tools_and_resources', '0002_alter_toolsandresourcespage_get_connected_button_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsandresourcespage',
            name='large_panels',
            field=wagtail.fields.StreamField([('panel', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('link_text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], required=False))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.CreateModel(
            name='ResourceAndLearningPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('large_panels', wagtail.fields.StreamField([('panel', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('link_text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], required=False))]))], blank=True, null=True, use_json_field=True)),
                ('go_back_prefix_text', models.CharField(default='Go Back to')),
                ('header_image', models.ForeignKey(blank=True, help_text='Header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]