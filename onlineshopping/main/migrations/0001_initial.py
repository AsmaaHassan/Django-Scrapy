# Generated by Django 2.1.3 on 2018-11-02 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=500, null=True)),
                ('item', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
