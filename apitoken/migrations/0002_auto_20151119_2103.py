# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('apitoken', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 19, 21, 2, 48, 283859)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='life',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='typ',
            field=models.CharField(default='standard', max_length=16, verbose_name=b'Type', choices=[(b'standard', b'Standard'), (b'app', b'App'), (b'otp', b'OTP'), (b'otp-verified', b'OTP-Verified')]),
            preserve_default=False,
        ),
    ]
