# Generated by Django 4.2.7 on 2024-08-06 21:22

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_individualprojectpage_intro'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField()),
            ],
        ),
        migrations.AddField(
            model_name='individualprojectpage',
            name='types',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='projects.projecttype'),
        ),
    ]
