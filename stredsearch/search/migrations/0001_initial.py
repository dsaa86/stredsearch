# Generated by Django 4.2.6 on 2023-10-18 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stackMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_prepend', models.CharField(max_length=200)),
                ('route_append', models.CharField(max_length=200)),
                ('filters', models.JSONField()),
                ('sort', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='stackRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_root', models.CharField(default='', max_length=200)),
                ('route', models.CharField(default='', max_length=200)),
                ('params', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='stackUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('display_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='stackQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on_stredsearch', models.DateTimeField(auto_now_add=True)),
                ('updated_on_stredsearch', models.DateTimeField(auto_now=True)),
                ('is_answered', models.BooleanField()),
                ('view_count', models.IntegerField()),
                ('answer_count', models.IntegerField()),
                ('score', models.IntegerField()),
                ('last_activity_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField()),
                ('last_edit_date', models.DateTimeField(blank=True)),
                ('question_id', models.IntegerField()),
                ('link', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='search.stackuser')),
            ],
        ),
    ]
