# Generated by Django 4.2 on 2023-05-30 02:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Account", "0012_profile_experience"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="experience",
            field=models.IntegerField(
                default=0, max_length=50, verbose_name="Years of Experience"
            ),
        ),
    ]