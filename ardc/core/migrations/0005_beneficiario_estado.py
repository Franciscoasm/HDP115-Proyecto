# Generated by Django 3.0.7 on 2020-07-16 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200715_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='estado',
            field=models.IntegerField(default=1),
        ),
    ]
