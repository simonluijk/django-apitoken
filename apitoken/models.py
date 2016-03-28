import hmac
import uuid
from hashlib import sha256
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings


class Token(models.Model):
    """
    A token for authentication with an API.
    """

    STANDARD = 'standard'
    APP = 'app'
    OTP_TMP = 'otp-tmp'
    OTP_VERIFIED = 'otp-verified'

    TYPE_CHOICES = (
        (STANDARD, 'Standard'),
        (APP, 'App'),
        (OTP_TMP, 'OTP Temp'),
        (OTP_VERIFIED, 'OTP Verified'),
    )

    LIFE = {
        STANDARD:       60 * 60 * 4,
        APP:            60 * 60 * 24 * 31,
        OTP_TMP:        60 * 10,
        OTP_VERIFIED:   60 * 60 * 4,
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='api_tokens')
    token = models.CharField(max_length=128, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    typ = models.CharField(verbose_name='Type', max_length=16,
                           choices=TYPE_CHOICES)
    expires = models.DateTimeField()
    life = models.PositiveIntegerField()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return '{0} token for {1} '.format(self.typ, self.user.email)

    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        if not self.token:
            self.generate_token()
            self.update_expires()

    @property
    def is_valid(self):
        return self.user.is_active and self.expires >= timezone.now()

    def update_expires(self):
        self.expires = timezone.now() + timedelta(seconds=self.life)

    def generate_token(self):
        self.token = hmac.new(uuid.uuid4().bytes, digestmod=sha256).hexdigest()
        self.life = self.LIFE[self.typ]
