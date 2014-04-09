try:
    from common import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'newsletter_archive',
        'USER': 'victor',
        'PASSWORD': 'lvxy',
        'HOST': '127.0.0.1',
        'PORT': '3306',    
    }
}
