# Generated by Django 2.2.5 on 2020-02-26 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("lists", "0003_auto_20200226_0929")]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="list",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]
