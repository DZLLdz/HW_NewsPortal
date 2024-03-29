# Generated by Django 5.0.1 on 2024-03-02 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Newsportalapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="post_author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="Newsportalapp.author",
                verbose_name="Имя Автора",
            ),
        ),
    ]
