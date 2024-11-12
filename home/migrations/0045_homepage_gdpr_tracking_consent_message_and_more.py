# Generated by Django 4.2.7 on 2024-11-08 00:49

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_alter_homepage_carousel_alter_homepage_e404_links_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='gdpr_tracking_consent_message',
            field=models.CharField(default='By clicking "I Agree", you consent to the use of cookies.'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='gdpr_tracking_message',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='gdpr_tracking_option_agree',
            field=models.CharField(default='I Agree'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='gdpr_tracking_option_disagree',
            field=models.CharField(default='I Disagree'),
        ),
    ]
