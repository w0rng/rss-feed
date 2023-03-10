# Generated by Django 3.2.9 on 2023-01-22 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_alter_feed_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='post',
            old_name='url',
            new_name='link',
        ),
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='feed.Tag'),
        ),
    ]
