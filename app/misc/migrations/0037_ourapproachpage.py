# Generated by Django 4.2.7 on 2024-10-29 16:49

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0026_delete_uploadedimage'),
        ('misc', '0036_generalpolicyownerpage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurApproachPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('banner_image', models.ForeignKey(blank=True, help_text='Header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]