# Generated by Django 4.2.6 on 2023-11-01 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_alter_stacktags_number_of_cached_instances'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stacktags',
            name='number_of_instances_on_so',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
