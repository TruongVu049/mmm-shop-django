# Generated by Django 5.0.4 on 2024-05-09 07:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_giohang'),
    ]

    operations = [
        migrations.AddField(
            model_name='giohang',
            name='ngaythem',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
