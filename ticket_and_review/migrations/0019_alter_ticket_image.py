# Generated by Django 4.0.4 on 2022-05-18 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_and_review", "0018_alter_ticket_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
