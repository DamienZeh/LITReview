# Generated by Django 4.0.4 on 2022-05-13 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_and_review', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(help_text=None, upload_to='', verbose_name='image'),
        ),
    ]