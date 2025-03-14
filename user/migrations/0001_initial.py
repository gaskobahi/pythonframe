# Generated by Django 5.1.4 on 2025-01-18 21:21

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by_id', models.UUIDField(blank=True, null=True)),
                ('updated_by_id', models.UUIDField(blank=True, null=True)),
                ('deleted_by_id', models.UUIDField(blank=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('display_name', models.CharField(max_length=255, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('admin_permission', models.BooleanField(default=False, verbose_name='Admin Permission')),
                ('permissions', models.JSONField(blank=True, null=True, verbose_name='Permissions')),
                ('field_permissions', models.JSONField(blank=True, null=True, verbose_name='Field Permissions')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by_id', models.UUIDField(blank=True, null=True)),
                ('updated_by_id', models.UUIDField(blank=True, null=True)),
                ('deleted_by_id', models.UUIDField(blank=True, null=True)),
                ('username', models.CharField(max_length=150, unique=True, verbose_name="Nom d'utilisateur")),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='Mot de passe')),
                ('is_active', models.BooleanField(default=True, verbose_name='Compte actif')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('last_access', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_accessed_users', to='custom_auth.authuser', verbose_name='Dernier accès')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='user.role', verbose_name='Rôle')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
