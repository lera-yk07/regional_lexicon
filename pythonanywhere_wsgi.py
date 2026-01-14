import os
import sys

path = os.path.expanduser('~/regional_lexicon')
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'regional_lexicon.production_settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()