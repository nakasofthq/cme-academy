# Generated by Django 4.2.9 on 2024-04-21 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
    ]
