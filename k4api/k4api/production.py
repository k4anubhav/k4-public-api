from .settings import *

ALLOWED_HOSTS = list(map(str.strip, os.environ['WEBSITE_HOSTNAME'].split(',')))
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = bool(os.getenv('DEBUG', 'false').lower() == 'true')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
