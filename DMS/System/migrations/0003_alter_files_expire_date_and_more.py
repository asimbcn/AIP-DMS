# Generated by Django 4.2.5 on 2023-09-26 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0002_files_uploaded_by_alter_files_expire_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 11, 18, 50, 6, 823702)),
        ),
        migrations.AlterField(
            model_name='version_control',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 11, 18, 50, 6, 823702)),
        ),
    ]
