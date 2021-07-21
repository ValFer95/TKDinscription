# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tkdinscription.vfeapps.fr']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db-inscription.sqlite3',
    }
}

# Email settings ONLY FOR TEST PURPOSE
EMAIL_HOST = 'umbriel.o2switch.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'mudoclub@tkdinscription.vfeapps.fr'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True