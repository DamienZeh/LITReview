# Generated by Django 4.0.4 on 2022-05-18 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_and_review', '0015_rename_author_ticket_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]