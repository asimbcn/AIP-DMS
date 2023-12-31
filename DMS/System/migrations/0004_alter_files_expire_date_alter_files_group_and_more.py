# Generated by Django 4.2.5 on 2023-09-26 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0003_alter_files_expire_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 11, 18, 53, 16, 870414)),
        ),
        migrations.AlterField(
            model_name='files',
            name='group',
            field=models.CharField(choices=[('management', 'Management'), ('all', 'All'), ('accounting', 'Accounting'), ('sales', 'Sales'), ('tech', 'Tech')], default='all', max_length=100),
        ),
        migrations.AlterField(
            model_name='version_control',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 11, 18, 53, 16, 870414)),
        ),
    ]
