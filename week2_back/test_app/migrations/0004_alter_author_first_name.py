# Generated by Django 4.2.13 on 2024-07-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_alter_author_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
    ]
