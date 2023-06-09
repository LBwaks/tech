# Generated by Django 4.2 on 2023-06-29 04:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("Account", "0020_experience"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="slug",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="experience",
            name="user_profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_experince",
                to="Account.profile",
                verbose_name="",
            ),
            preserve_default=False,
        ),
    ]
