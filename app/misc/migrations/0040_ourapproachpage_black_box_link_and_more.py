# Generated by Django 4.2.7 on 2024-10-29 19:43

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0039_alter_ourapproachpage_what_we_do_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='ourapproachpage',
            name='black_box_link',
            field=wagtail.fields.StreamField([('page', 0), ('url', 1), ('document', 2), ('other', 3)], blank=True, block_lookup={0: ('wagtail.blocks.PageChooserBlock', (), {}), 1: ('wagtail.blocks.URLBlock', (), {}), 2: ('wagtail.documents.blocks.DocumentChooserBlock', (), {}), 3: ('wagtail.blocks.CharBlock', (), {'help_text': "Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."})}),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='black_box_link_text',
            field=models.CharField(default='Partner With Us'),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='black_box_title',
            field=models.CharField(default='Partner with us to create and use open map data'),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='hot_envisions_items',
            field=wagtail.fields.StreamField([('item', 0)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'max_num': 3, 'min_num': 3})}),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='hot_envisions_title',
            field=models.CharField(default='HOT Envisions a World in Which...'),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='our_toolbox_items',
            field=wagtail.fields.StreamField([('block', 2)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 1: ('wagtail.blocks.CharBlock', (), {}), 2: ('wagtail.blocks.StructBlock', [[('icon', 0), ('text', 1)]], {})}),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='our_toolbox_title',
            field=models.CharField(default='Our Toolbox'),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='red_box_link',
            field=wagtail.fields.StreamField([('page', 0), ('url', 1), ('document', 2), ('other', 3)], blank=True, block_lookup={0: ('wagtail.blocks.PageChooserBlock', (), {}), 1: ('wagtail.blocks.URLBlock', (), {}), 2: ('wagtail.documents.blocks.DocumentChooserBlock', (), {}), 3: ('wagtail.blocks.CharBlock', (), {'help_text': "Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live."})}),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='red_box_link_text',
            field=models.CharField(default='Get Involved'),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='red_box_title',
            field=models.CharField(default='Check out the many opportunities to get involved with HOT'),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='what_happens_items',
            field=wagtail.fields.StreamField([('block', 2)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 1: ('wagtail.blocks.CharBlock', (), {}), 2: ('wagtail.blocks.StructBlock', [[('icon', 0), ('text', 1)]], {})}),
        ),
        migrations.AddField(
            model_name='ourapproachpage',
            name='what_happens_title',
            field=models.CharField(default='What Happens Because of Our Work'),
        ),
    ]