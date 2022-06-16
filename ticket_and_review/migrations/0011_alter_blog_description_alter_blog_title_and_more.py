# Generated by Django 4.0.4 on 2022-05-15 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_and_review", "0010_remove_photo_caption"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="description",
            field=models.TextField(
                max_length=5000, verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="title",
            field=models.CharField(max_length=128, verbose_name="Titre"),
        ),
        migrations.AlterField(
            model_name="photo",
            name="image",
            field=models.ImageField(upload_to="", verbose_name="Image"),
        ),
    ]
