# Generated by Django 4.2 on 2023-05-04 03:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Job", "0003_alter_job_reference_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="reference_id",
            field=models.CharField(unique=True, verbose_name="reference_id"),
        ),
    ]
