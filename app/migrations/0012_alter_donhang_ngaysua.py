# Generated by Django 5.0.4 on 2024-06-01 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_phuongthucthanhtoan_trangthaidonhang_chitietdonhang_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donhang',
            name='ngaysua',
            field=models.DateTimeField(null=True),
        ),
    ]
