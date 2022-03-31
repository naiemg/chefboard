# Generated by Django 3.2.12 on 2022-03-31 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stripeCustomerId',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='stripeSubscriptionId',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]