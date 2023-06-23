# Generated by Django 4.2 on 2023-06-21 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Job", "0016_alter_jobimage_job"),
    ]

    operations = [
        migrations.AlterField(
            model_name="savedjob",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="saved_job",
                to="Job.job",
            ),
        ),
    ]