# Generated by Django 4.2 on 2023-05-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Job", "0012_job_industry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="industry",
            field=models.CharField(
                choices=[("Hotel", "Hotel"), ("Home", "Home")],
                max_length=50,
                verbose_name="Industry",
            ),
        ),
    ]
