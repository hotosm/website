# Generated by Django 4.2.7 on 2024-07-16 21:15

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rfp', '0003_requestforproposalownerpage_aside_block_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestforproposalownerpage',
            name='no_rfps_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='requestforproposalownerpage',
            name='no_rfps_title',
            field=models.CharField(default='There are no current RFPs.'),
        ),
    ]
