# Generated by Django 2.2.20 on 2021-10-15 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcvserver', '0009_choice_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ballot_identifier', models.CharField(default=None, max_length=24)),
            ],
        ),
    ]