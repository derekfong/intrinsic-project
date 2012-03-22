#!/usr/bin/env python
import os, sys

# make sure app's modules can be found
sys.path.append('/var/www/intrinsic-project')
sys.path.append('/var/www/intrinsic-project/SOL')
os.environ['DJANGO_SETTINGS_MODULE'] = 'SOL.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
