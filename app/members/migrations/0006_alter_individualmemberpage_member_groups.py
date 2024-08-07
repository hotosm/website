# Generated by Django 4.2.7 on 2024-07-09 22:45

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_individualmemberpage_member_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualmemberpage',
            name='member_groups',
            field=wagtail.fields.StreamField([('member_group', wagtail.blocks.StructBlock([('group', wagtail.blocks.PageChooserBlock(page_type=['members.MemberGroupPage'])), ('role', wagtail.blocks.CharBlock())]))], blank=True, null=True, use_json_field=True),
        ),
    ]
