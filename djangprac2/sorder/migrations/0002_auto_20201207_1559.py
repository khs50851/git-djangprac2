# Generated by Django 3.1.4 on 2020-12-07 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sorder',
            name='memo',
            field=models.TextField(blank=True, null=True, verbose_name='메모'),
        ),
        migrations.AddField(
            model_name='sorder',
            name='status',
            field=models.CharField(default='대기중', max_length=32, verbose_name='상태'),
        ),
    ]
