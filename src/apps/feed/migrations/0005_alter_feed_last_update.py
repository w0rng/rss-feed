# Generated by Django 3.2.9 on 2023-02-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20230211_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
