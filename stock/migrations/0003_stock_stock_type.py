# Generated by Django 2.2.9 on 2021-01-29 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20210130_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='stock_type',
            field=models.CharField(max_length=10, null=True),
        ),
    ]