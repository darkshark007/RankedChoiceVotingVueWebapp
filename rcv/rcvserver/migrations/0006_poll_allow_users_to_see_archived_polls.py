# Generated by Django 2.2.20 on 2021-06-06 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcvserver', '0005_poll_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='allow_users_to_see_archived_polls',
            field=models.BooleanField(default=True),
        ),
    ]
