# Generated by Django 4.2.15 on 2024-10-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_alter_products_options_alter_products_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
    ]
