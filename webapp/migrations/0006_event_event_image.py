# Generated by Django 2.2.28 on 2025-03-23 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20250322_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]
