from django.conf import settings

TOKEN_TYPES = getattr(settings, 'TOKEN_TYPES', (
    {
        'key': 'standard',
        'label': 'Standard',
        'life': 60 * 60 * 4,
    },
    {
        'key': 'app',
        'label': 'App',
        'life': 60 * 60 * 24 * 31,
    },
    {
        'key': 'otp-tmp',
        'label': 'OTP Temp',
        'life': 60 * 10,
    },
    {
        'key': 'otp-verified',
        'label': 'OTP Verified',
        'life': 60 * 60 * 4,
    }
))
