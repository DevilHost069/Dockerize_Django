# Generated by Django 3.2.6 on 2022-01-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0004_remove_userprofile_listingads'),
        ('marketapp', '0012_auto_20220122_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingproducts',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to='usersapp.Userprofile'),
        ),
        migrations.AddField(
            model_name='listingproducts',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to='usersapp.Userprofile'),
        ),
    ]
