# Generated by Django 4.2.5 on 2023-10-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_userinfo_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
