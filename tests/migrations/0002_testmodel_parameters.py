# Generated by Django 3.1.1 on 2020-09-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='parameters',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]