# Generated by Django 4.2 on 2023-05-05 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Job", "0006_alter_job_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="job_images/default_image.jpg",
                        null=True,
                        upload_to="job_images/",
                        verbose_name="Job Images",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Job.job",
                        verbose_name="",
                    ),
                ),
            ],
            options={
                "verbose_name": "JobImage",
                "verbose_name_plural": "JobImages",
            },
        ),
    ]
