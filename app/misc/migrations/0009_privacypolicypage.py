# Generated by Django 4.2.7 on 2024-08-01 16:35

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('misc', '0008_codeofconductpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicyPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('body_text', wagtail.fields.RichTextField(blank=True)),
                ('our_policies_title', models.CharField(default='Our Policies')),
                ('our_policies_links', wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())]))]))], blank=True, help_text='Links to be shown under the Our Policies section.', null=True, use_json_field=True)),
                ('question_block_title', models.CharField(default='Have a question about the code of conduct?')),
                ('question_block_button_text', models.CharField(default='Contact Community Working Group')),
                ('question_block_button_link', wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock())], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
