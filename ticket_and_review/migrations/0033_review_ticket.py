# Generated by Django 4.0.4 on 2022-05-26 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_and_review', '0032_remove_review_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket_and_review.ticket'),
        ),
    ]