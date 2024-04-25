# Generated by Django 4.1 on 2024-04-25 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("checking", "0027_alter_attendance_teacher"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to=settings.AUTH_USER_MODEL,
                to_field="username",
            ),
        ),
    ]