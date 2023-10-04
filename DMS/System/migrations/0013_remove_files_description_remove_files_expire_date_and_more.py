# Generated by Django 4.2.5 on 2023-10-03 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0012_files_new_version_version_control_new_version_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='description',
        ),
        migrations.RemoveField(
            model_name='files',
            name='expire_date',
        ),
        migrations.RemoveField(
            model_name='version_control',
            name='changes',
        ),
        migrations.RemoveField(
            model_name='version_control',
            name='expire_date',
        ),
        migrations.AddField(
            model_name='files',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='version_control',
            name='version',
            field=models.IntegerField(default='2'),
        ),
    ]
