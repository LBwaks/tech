# Generated by Django 4.2 on 2023-06-05 06:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Application", "0006_alter_application_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="charge",
            field=models.IntegerField(verbose_name="Fees"),
        ),
    ]
