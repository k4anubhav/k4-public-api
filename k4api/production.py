from .settings import *

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = bool(os.getenv('DEBUG', 'false').lower() == 'true')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
