# Generated by Django 4.2.6 on 2023-10-23 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_alter_stackquestion_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stacksearchterms',
            name='search_term',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='stredsearchquestion',
            name='search_term',
            field=models.ManyToManyField(to='search.stacksearchterms'),
        ),
    ]