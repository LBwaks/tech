# Generated by Django 4.2 on 2023-06-25 06:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Application", "0010_alter_rating_ratings"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Rating",
        ),
    ]
