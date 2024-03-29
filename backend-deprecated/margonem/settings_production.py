import os

if 'HTTPS' in os.environ:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    USE_X_FORWARDED_HOST = True

# CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv(), default=())

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}