# Generated by Django 5.1.5 on 2025-03-04 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('audiozone_sys', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('photozone_sys', '0003_imgs4designscomments_photoscomments'),
        ('projectzone_sys', '0003_projectscomments'),
        ('videozone_sys', '0002_templatevideo_shortvideo_likes_longvideocomments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(blank=True, max_length=255)),
                ('authentificator', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('last_login_at', models.DateTimeField(auto_now=True)),
                ('custom_pref', models.JSONField(default=dict)),
                ('audio', models.ManyToManyField(blank=True, to='audiozone_sys.audio')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('music', models.ManyToManyField(blank=True, to='audiozone_sys.music')),
                ('photos', models.ManyToManyField(blank=True, to='photozone_sys.photos')),
                ('project', models.ManyToManyField(blank=True, to='projectzone_sys.project')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('videos_long', models.ManyToManyField(blank=True, to='videozone_sys.longvideo')),
                ('videos_short', models.ManyToManyField(blank=True, to='videozone_sys.shortvideo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
