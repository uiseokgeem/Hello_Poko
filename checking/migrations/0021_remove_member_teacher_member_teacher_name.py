# Generated by Django 4.1 on 2024-03-04 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("checking", "0020_remove_member_etc_remove_member_tardy"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="teacher",
        ),
        migrations.AddField(
            model_name="member",
            name="teacher_name",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="checking.teacher",
                to_field="teacher_name",
            ),
            preserve_default=False,
        ),
    ]
