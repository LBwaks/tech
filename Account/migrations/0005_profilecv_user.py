# Generated by Django 4.2 on 2023-05-12 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Account", "0004_remove_profilecv_user_profilecv_created_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profilecv",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
