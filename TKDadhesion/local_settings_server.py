# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db-inscription.sqlite3',
    }
}


# Email settings ONLY FOR TEST PURPOSE
EMAIL_HOST = 'tkd.vfeapps.fr'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'mudoclubarg@tkd.vfeapps.fr'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False