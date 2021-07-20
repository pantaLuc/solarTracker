# Generated by Django 3.2.5 on 2021-07-19 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'admin'), ('client', 'client')], default='client', max_length=7, null=True),
        ),
    ]
