# Generated by Django 4.0.2 on 2022-03-07 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='val',
            field=models.BooleanField(default=False),
        ),
    ]
