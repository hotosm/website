# Generated by Django 4.2.7 on 2024-08-01 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0009_privacypolicypage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypolicypage',
            name='question_block_button_text',
            field=models.CharField(default='Contact HOT'),
        ),
        migrations.AlterField(
            model_name='privacypolicypage',
            name='question_block_title',
            field=models.CharField(default='Have a question about the privacy policy?'),
        ),
    ]
