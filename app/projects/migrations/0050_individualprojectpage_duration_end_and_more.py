# Generated by Django 4.2.7 on 2025-03-21 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0049_alter_individualprojectpage_partner_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualprojectpage',
            name='duration_end',
            field=models.DateField(blank=True, help_text="The end date of the project; if an end is provided but no start, this will dislpay as 'Until [end date]'.", null=True),
        ),
        migrations.AddField(
            model_name='individualprojectpage',
            name='duration_start',
            field=models.DateField(blank=True, help_text="The start date of the project; if a start is provided but no end, this will display as '[start date] ー Ongoing'.", null=True),
        ),
        migrations.AlterField(
            model_name='individualprojectpage',
            name='duration',
            field=models.CharField(blank=True, help_text='Any text-based description of duration should be here; dates should ideally use the Duration Start and End fields.'),
        ),
    ]
