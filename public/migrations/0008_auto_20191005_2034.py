# Generated by Django 2.2.2 on 2019-10-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0007_auto_20191005_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='missingperson',
            name='img',
            field=models.ImageField(blank=True, upload_to='missing_imgs/'),
        ),
        migrations.AddField(
            model_name='unidentifiedbodies',
            name='img',
            field=models.ImageField(blank=True, upload_to='unidentBodies_imgs/'),
        ),
    ]
