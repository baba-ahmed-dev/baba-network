# Generated by Django 4.0.2 on 2022-03-04 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_post_options_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, default='media/defaultProfile.png', null=True, upload_to='photos%d%y%m'),
        ),
    ]
