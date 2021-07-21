# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db-inscription.sqlite3',
    }
}

# Email settings ONLY FOR TEST PURPOSE
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'    # pour afficher dans la console Ne pas mettre en production, seulement pour le dev
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/test-mail' # change this to a proper location
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False