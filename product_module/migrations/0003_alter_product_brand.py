# Generated by Django 4.0.6 on 2022-08-07 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0002_productbrand_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_brand', to='product_module.productbrand', verbose_name='برند'),
        ),
    ]
