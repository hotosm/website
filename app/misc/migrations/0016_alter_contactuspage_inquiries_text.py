# Generated by Django 4.2.7 on 2024-08-26 21:10

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0015_contactuspage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactuspage',
            name='inquiries_text',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]