# Generated by Django 4.2 on 2023-05-04 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Application", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
