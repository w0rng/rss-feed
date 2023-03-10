# Generated by Django 3.2.9 on 2023-02-11 11:00

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20230122_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='interval',
            field=models.PositiveSmallIntegerField(default=600, help_text='in sec', validators=[django.core.validators.MinValueValidator(600)]),
        ),
        migrations.AddField(
            model_name='feed',
            name='last_update',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
