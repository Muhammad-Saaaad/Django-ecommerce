# Generated by Django 5.1.1 on 2024-10-04 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="like_counts",
            field=models.IntegerField(default=0),
        ),
    ]
