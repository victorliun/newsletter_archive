try:
    from settings_set.dev import *
except ImportError:
    pass
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9!7nw)$=9qv*qyrtesy#&_2+$*m0tv6+2cvdz+rzigwz3%z9f&'

import sys

if 'test' in sys.argv:
    # Use nose to run all tests
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    INSTALLED_APPS += ('django_nose',)
    # Tell nose to measure coverage on these apps
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=archive,',
        '--verbosity=2',
    ]

