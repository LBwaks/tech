# Generated by Django 4.2 on 2023-05-12 07:44

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("Account", "0010_alter_profile_id_passport"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="tell",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None, unique=True
            ),
        ),
    ]
