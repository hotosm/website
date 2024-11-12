# Generated by Django 4.2.7 on 2024-10-10 17:41

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0033_alter_multimediapage_video_previews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeofconductpage',
            name='our_policies_links',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))]))]))], blank=True, help_text='Links to be shown under the Our Policies section.', null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='codeofconductpage',
            name='question_block_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='contactuspage',
            name='dogear_box_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='contactuspage',
            name='office_locations',
            field=wagtail.fields.StreamField([('block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(blank=True, null=True, required=False)), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, null=True, required=False)), ('description', wagtail.blocks.RichTextBlock(blank=True, null=True, required=False))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='dataprinciplespage',
            name='footer_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='documentcollectionpage',
            name='documents',
            field=wagtail.fields.StreamField([('block', wagtail.blocks.StructBlock([('icon', wagtail.images.blocks.ImageChooserBlock(blank=True, null=True, required=False)), ('title', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))])), ('description', wagtail.blocks.RichTextBlock(blank=True, null=True, required=False))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='documentcollectionpage',
            name='sidebar_box_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='joinourconversationpage',
            name='black_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='joinourconversationpage',
            name='code_of_conduct_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='joinourconversationpage',
            name='red_box_link_url',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='livingstrategypage',
            name='downloads',
            field=wagtail.fields.StreamField([('block', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], required=False))]))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='multimediapage',
            name='image_view_all_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='multimediapage',
            name='map_view_all_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='multimediapage',
            name='video_view_all_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='privacypolicypage',
            name='our_policies_links',
            field=wagtail.fields.StreamField([('blocks', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))]))]))], blank=True, help_text='Links to be shown under the Our Policies section.', null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='privacypolicypage',
            name='question_block_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='salaryframeworkpage',
            name='sidebar_block_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='workforhotpage',
            name='opportunities_button_link',
            field=wagtail.fields.StreamField([('page', wagtail.blocks.PageChooserBlock()), ('url', wagtail.blocks.URLBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('other', wagtail.blocks.CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."))], blank=True, use_json_field=True),
        ),
    ]