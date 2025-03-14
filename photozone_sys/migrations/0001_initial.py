# Generated by Django 5.1.5 on 2025-01-24 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.FileField(upload_to='')),
                ('size', models.CharField(max_length=60)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('share_link', models.TextField()),
                ('share_title', models.CharField(max_length=255)),
            ],
        ),
    ]
