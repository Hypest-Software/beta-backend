# Generated by Django 3.1.3 on 2020-11-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beta_apis', '0009_auto_20201121_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
