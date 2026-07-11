from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0022_remove_individualmemberpage_intro"),
    ]

    operations = [
        migrations.AddField(
            model_name="membergroupownerpage",
            name="filter_other_label",
            field=models.CharField(
                default="Other",
                help_text="Label for members not assigned to any mapping hub region.",
            ),
        ),
    ]
