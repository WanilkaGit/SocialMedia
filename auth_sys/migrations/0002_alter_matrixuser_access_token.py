# Generated by Django 5.1.5 on 2025-02-02 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_sys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrixuser',
            name='access_token',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
