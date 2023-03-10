# Generated by Django 4.1.5 on 2023-01-10 15:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("django_school", "0002_remove_parent_student_student_parents"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
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
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("created_date", models.DateField()),
                ("due_date", models.DateField()),
                (
                    "classroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_school.classroom",
                    ),
                ),
                (
                    "grade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_school.grade",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_school.subject",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Announcements",
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
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("date", models.DateField()),
                (
                    "grade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_school.grade",
                    ),
                ),
            ],
        ),
    ]
