# Generated by Django 3.2.7 on 2021-09-27 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_image',
            field=models.CharField(default='https://dummyimage.com/450x300/dee2e6/6c757d.jpg', max_length=300),
        ),
    ]
