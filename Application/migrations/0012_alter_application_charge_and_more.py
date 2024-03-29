# Generated by Django 4.2 on 2023-07-26 03:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Application", "0011_delete_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="charge",
            field=models.IntegerField(verbose_name="Fees (ksh)"),
        ),
        migrations.AlterField(
            model_name="application",
            name="description",
            field=ckeditor.fields.RichTextField(
                verbose_name="Why You charge Above Fees!"
            ),
        ),
    ]
