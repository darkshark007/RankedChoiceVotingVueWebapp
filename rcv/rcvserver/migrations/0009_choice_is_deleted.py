# Generated by Django 2.2.20 on 2021-06-28 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcvserver', '0008_poll_ballots_must_be_full'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
