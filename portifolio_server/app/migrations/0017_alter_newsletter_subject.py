# Generated by Django 5.0.4 on 2024-06-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='subject',
            field=models.CharField(max_length=250, verbose_name='Email Subject'),
        ),
    ]
