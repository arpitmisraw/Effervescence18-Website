# Generated by Django 2.0.2 on 2018-07-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0026_auto_20180727_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularuser',
            name='fb_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]