# Generated by Django 4.2 on 2023-06-27 04:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Account", "0016_education"),
    ]

    operations = [
        migrations.AddField(
            model_name="education",
            name="description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Description"
            ),
        ),
    ]
