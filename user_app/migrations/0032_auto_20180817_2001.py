# Generated by Django 2.0.6 on 2018-08-17 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0031_auto_20180808_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
