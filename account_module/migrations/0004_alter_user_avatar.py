# Generated by Django 4.0.6 on 2022-08-13 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0003_user_about_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile', verbose_name='تصویر اواتار'),
        ),
    ]