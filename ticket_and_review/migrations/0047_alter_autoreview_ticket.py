# Generated by Django 4.0.4 on 2022-06-07 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_and_review", "0046_alter_autoreview_ticket"),
    ]

    operations = [
        migrations.AlterField(
            model_name="autoreview",
            name="ticket",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ticket_and_review.ticket",
            ),
        ),
    ]
