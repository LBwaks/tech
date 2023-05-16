# Generated by Django 4.2 on 2023-05-06 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Job", "0007_jobimage"),
    ]

    operations = [
        
        migrations.AlterModelOptions(
            name="job",
            options={
                "ordering": ["-created"],
                "verbose_name": "Job",
                "verbose_name_plural": "Jobs",
            },
        ),
        migrations.AlterField(
            model_name="job",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="Job.category",
                verbose_name="Category",
            ),
        ),
        migrations.CreateModel(
            name="SavedJob",
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
                ("saved_date", models.DateTimeField(auto_now_add=True)),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Job.job"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "SavedJob",
                "verbose_name_plural": "SavedJobs",
                "unique_together": {("user", "job")},
            },
        ),
    ]
