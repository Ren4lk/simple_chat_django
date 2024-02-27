# Generated by Django 5.0 on 2024-02-11 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('ru', 'Russian')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=10, null=True),
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
    ]
