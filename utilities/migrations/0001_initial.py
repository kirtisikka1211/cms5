# Generated by Django 2.2.24 on 2023-05-19 13:40

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('category', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=100)),
                ('creationTime', models.DateTimeField(blank=True, null=True)),
                ('lastEditTime', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='TokenCreator', to=settings.AUTH_USER_MODEL)),
                ('lastEditor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='TokenLastEditor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
        migrations.CreateModel(
            name='Mailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100, null=True)),
                ('generationEmailDate', models.DateField(default=None, verbose_name='Date')),
                ('generationEmailTime', models.CharField(max_length=20, verbose_name='Time')),
                ('subject', models.CharField(max_length=50, verbose_name='Email Message subject')),
                ('threadMessage', ckeditor.fields.RichTextField(max_length=5000, verbose_name='Email Message')),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Form')),
            ],
            options={
                'verbose_name': 'Mailer',
                'verbose_name_plural': 'Mailer',
            },
        ),
    ]
