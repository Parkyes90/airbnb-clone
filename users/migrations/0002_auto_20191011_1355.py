# Generated by Django 2.2.5 on 2019-10-11 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        )
    ]