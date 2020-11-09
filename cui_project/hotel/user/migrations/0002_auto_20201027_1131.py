# Generated by Django 2.2.12 on 2020-10-27 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=256, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='real_name',
            field=models.CharField(default='', max_length=30, verbose_name='真实姓名'),
        ),
    ]