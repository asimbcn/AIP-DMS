# Generated by Django 4.2.5 on 2023-11-06 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0020_temp_ocr'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_ocr',
            name='file_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]