# Generated by Django 4.0.4 on 2022-06-01 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_and_review', '0034_autoreview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autoreview',
            name='ticket',
        ),
    ]
