# Generated by Django 2.2.5 on 2019-11-11 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0004_auto_20191111_1357")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_secret",
            field=models.CharField(blank=True, default="", max_length=120),
        )
    ]
