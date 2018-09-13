# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-09-13 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('submission', '0027_auto_20180806_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_type', models.CharField(choices=[('minor', 'Minor'), ('major', 'Major')], max_length=20)),
                ('new_author', models.BooleanField(default=False)),
                ('revision_date', models.DateTimeField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('article', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submission.Article')),
                ('parent_article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updates', to='submission.Article')),
            ],
        ),
    ]
