# Generated by Django 4.2 on 2023-05-12 03:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile",
            field=models.ImageField(
                blank=True,
                default="default_profile.png",
                null=True,
                upload_to="profiles",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["jpg", "png", "jpeg"]
                    )
                ],
                verbose_name="Profile Picture",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_type",
            field=models.CharField(
                choices=[("Individual", "Individual"), ("Agency", "Agency")],
                max_length=50,
                verbose_name="User Type",
            ),
        ),
    ]
