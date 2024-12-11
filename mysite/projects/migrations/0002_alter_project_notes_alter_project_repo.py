# Generated by Django 4.2.7 on 2024-12-10 02:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="notes",
            field=models.CharField(
                blank=True,
                default="",
                max_length=100,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        10, "Notes must be greater than 5 characters"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="repo",
            field=models.URLField(
                blank=True,
                default="",
                help_text="Provide a valid URL for the project repository.",
            ),
        ),
    ]