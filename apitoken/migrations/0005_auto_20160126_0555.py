# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitoken', '0004_auto_20160119_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='typ',
            field=models.CharField(max_length=16, verbose_name=b'Type', choices=[(b'standard', b'Standard'), (b'app', b'App'), (b'otp-tmp', b'OTP Temp'), (b'otp-verified', b'OTP Verified')]),
        ),
    ]
