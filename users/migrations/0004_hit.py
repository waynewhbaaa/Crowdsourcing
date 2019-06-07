# Generated by Django 2.1.7 on 2019-06-06 18:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190605_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='HIT',
            fields=[
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('session', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Session ID')),
            ],
        ),
    ]
