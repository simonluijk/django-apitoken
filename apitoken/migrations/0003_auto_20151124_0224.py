# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('apitoken', '0002_auto_20151119_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.ForeignKey(related_name='api_tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
