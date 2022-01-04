# Generated by Django 3.2.6 on 2022-01-03 09:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('marketapp', '0005_auto_20220103_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingimages',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='listingimages',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
