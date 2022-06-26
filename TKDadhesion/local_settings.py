# DEBUT DES LIGNES A DECOMMENTER POUR LES TESTS DE DEV - ces lignes sont utilisées pour recetter les fonctions d'envoi de mails
# from pathlib import Path
# import os
#
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# FIN DES LIGNES A DECOMMENTER POUR LES TESTS DE DEV


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
# DEBUT DES LIGNES A COMMENTER POUR LA MEP
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp/test-mail') # change this to a proper location
# FIN DES LIGNES A COMMENTER POUR LA MEP
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False