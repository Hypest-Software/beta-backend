# Generated by Django 3.1.3 on 2020-11-21 21:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('beta_apis', '0004_auto_20201121_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('describe', models.CharField(blank=True, max_length=255, null=True)),
                ('photo_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'report',
            },
        ),
    ]
