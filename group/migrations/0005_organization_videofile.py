# Generated by Django 3.1.7 on 2021-04-18 21:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_auto_20210418_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='videofile',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]