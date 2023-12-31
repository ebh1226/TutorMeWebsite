# Generated by Django 3.2.17 on 2023-04-02 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorme11', '0002_tutorme_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='classes',
            field=models.ManyToManyField(blank=True, related_name='users', to='tutorme11.Class'),
        ),
    ]
