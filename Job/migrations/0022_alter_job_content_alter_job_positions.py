# Generated by Django 4.2 on 2023-06-27 04:08

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Job", "0021_rename_job_images_jobimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="content",
            field=ckeditor.fields.RichTextField(verbose_name="Job Description"),
        ),
        migrations.AlterField(
            model_name="job",
            name="positions",
            field=models.IntegerField(verbose_name="Available Slots"),
        ),
    ]
