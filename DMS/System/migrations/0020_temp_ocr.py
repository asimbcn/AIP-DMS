# Generated by Django 4.2.5 on 2023-11-06 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0019_files_file_content_version_control_file_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_OCR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='files/OCR/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
