# Generated by Django 4.2.7 on 2024-07-15 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualrequestforproposalpage',
            name='post_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='individualrequestforproposalpage',
            name='application_close_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
