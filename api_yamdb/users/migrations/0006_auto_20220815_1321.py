# Generated by Django 2.2.16 on 2022-08-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220815_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, default=0, max_length=40),
        ),
    ]
