# Generated by Django 3.2.7 on 2021-09-16 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_contact_customer_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.CharField(max_length=201),
        ),
    ]
