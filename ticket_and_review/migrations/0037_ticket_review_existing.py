# Generated by Django 4.0.5 on 2022-06-05 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_and_review", "0036_autoreview_ticket"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="review_existing",
            field=models.BooleanField(default=False),
        ),
    ]
