# Generated by Django 5.1.3 on 2024-11-24 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studentportal", "0003_discussion_timetable"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
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
                ("date", models.DateField()),
                ("is_present", models.BooleanField(default=False)),
                ("remarks", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendances",
                        to="studentportal.student",
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "date")},
            },
        ),
    ]
