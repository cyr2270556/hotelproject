# Generated by Django 2.2.12 on 2020-11-05 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201103_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotelname', models.CharField(max_length=50, verbose_name='酒店名')),
                ('roomnumber', models.CharField(max_length=30, verbose_name='房间号')),
                ('roomprice', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='房间价格')),
                ('is_alive', models.BooleanField(default=True, verbose_name='是否有效')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
        ),
    ]