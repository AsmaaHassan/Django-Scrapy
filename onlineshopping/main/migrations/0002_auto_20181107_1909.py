# Generated by Django 2.1.3 on 2018-11-07 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scrapyitem',
            old_name='item',
            new_name='data',
        ),
    ]
