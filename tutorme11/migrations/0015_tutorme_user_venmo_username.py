# Generated by Django 3.2.17 on 2023-05-02 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorme11', '0014_auto_20230421_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorme_user',
            name='venmo_username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
