# Generated by Django 4.2 on 2023-08-02 05:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Job", "0023_remove_job_positions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="reference_id",
            field=models.CharField(
                max_length=250, unique=True, verbose_name="reference_id"
            ),
        ),
    ]