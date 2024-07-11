# Generated by Django 4.2.7 on 2024-07-08 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_hotsearchablepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPagePage',
            fields=[
                ('hotsearchablepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.hotsearchablepage')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.hotsearchablepage',),
        ),
    ]
