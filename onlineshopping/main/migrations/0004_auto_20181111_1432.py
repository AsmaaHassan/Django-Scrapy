# Generated by Django 2.1.3 on 2018-11-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181110_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='scrapyitem',
            name='unique_id',
        ),
    ]
