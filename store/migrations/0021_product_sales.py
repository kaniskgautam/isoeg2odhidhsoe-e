# Generated by Django 3.2.7 on 2021-11-24 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.IntegerField(default=0),
        ),
    ]