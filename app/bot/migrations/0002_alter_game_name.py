# Generated by Django 3.2.8 on 2021-11-17 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]