# Generated by Django 4.0.2 on 2022-03-15 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_follow_val'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, default='defaultProfile.png', null=True, upload_to='photos%d%y%m'),
        ),
    ]