# Generated by Django 4.0.4 on 2022-05-25 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_and_review", "0029_alter_ticket_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="./", verbose_name="image"
            ),
        ),
    ]
