# Generated by Django 3.2.7 on 2021-09-24 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
