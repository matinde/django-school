# Generated by Django 4.1.5 on 2023-01-09 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_school", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="parent", name="student",),
        migrations.AddField(
            model_name="student",
            name="parents",
            field=models.ManyToManyField(
                blank=True, related_name="students", to="django_school.parent"
            ),
        ),
    ]