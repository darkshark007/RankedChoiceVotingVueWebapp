# Generated by Django 2.2.20 on 2021-06-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcvserver', '0003_poll_limit_choices_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='users_can_add_choices',
            field=models.CharField(choices=[('always', 'always'), ('open', 'open'), ('never', 'never')], default='never', max_length=6),
        ),
    ]
