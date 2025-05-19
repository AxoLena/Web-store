import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'store.settings'
django.setup()