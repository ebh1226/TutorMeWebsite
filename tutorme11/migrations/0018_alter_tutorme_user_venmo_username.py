# Generated by Django 3.2.17 on 2023-05-02 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorme11', '0017_alter_tutorme_user_venmo_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorme_user',
            name='venmo_username',
            field=models.CharField(blank=True, default='pgzdq', max_length=50, null=True),
        ),
    ]