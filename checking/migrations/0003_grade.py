# Generated by Django 4.1 on 2024-02-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checking", "0002_attendance"),
    ]

    operations = [
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField()),
            ],
        ),
    ]
