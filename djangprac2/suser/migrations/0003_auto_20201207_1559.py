# Generated by Django 3.1.4 on 2020-12-07 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suser', '0002_suser_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='비밀번호'),
        ),
    ]
