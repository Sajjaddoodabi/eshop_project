# Generated by Django 4.0.6 on 2022-08-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]