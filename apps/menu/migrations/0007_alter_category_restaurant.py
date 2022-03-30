# Generated by Django 3.2.12 on 2022-03-29 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_menuitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='menu.restaurant'),
        ),
    ]