# Generated by Django 4.1 on 2024-02-20 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("checking", "0007_grade"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="grade_code",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="checking.grade",
            ),
            preserve_default=False,
        ),
    ]
