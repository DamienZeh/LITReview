# Generated by Django 4.0.4 on 2022-05-26 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_and_review', '0030_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ticket_and_review.ticket'),
        ),
    ]