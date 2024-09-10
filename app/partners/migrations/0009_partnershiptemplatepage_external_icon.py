# Generated by Django 4.2.7 on 2024-08-13 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('partners', '0008_ourpartnerspage_call_to_action_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnershiptemplatepage',
            name='external_icon',
            field=models.ForeignKey(blank=True, help_text='An icon to be shown on the Partner With Us page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]