# Generated by Django 4.0.5 on 2022-06-08 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theChowkidarApp', '0005_alter_accountverify_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_expair',
            field=models.BooleanField(default=False),
        ),
    ]
