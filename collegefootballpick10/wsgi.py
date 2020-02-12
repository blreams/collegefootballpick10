"""
WSGI config for collegefootballpick10 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

##############################################################################
# I found this on a readthedocs page for modwsgi that shows how to run
# activate_this.py for a virtualenv with apache.
##############################################################################
python_home = '/home/blreams/.virtualenvs/cdcpool'
activate_this = python_home + '/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))
##############################################################################

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collegefootballpick10.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
