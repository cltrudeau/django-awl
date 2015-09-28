# awl.logtools.py

from wrench.logtools.utils import default_logging_dict

# =============================================================================

def django_logging_dict(log_dir, handlers=['file'], filename='debug.log'):
    """Extends :func:`wrench.logtools.utils.default_logging_dict` with django
    specific values.
    """
    d = default_logging_dict(log_dir, handlers, filename)
    d['handlers'].update({
        'mail_admins':{
            'level':'ERROR',
            'class':'django.utils.log.AdminEmailHandler',
        }
    })
    d['loggers'].update({
        'django.db.backends': { # stop SQL debug from going to main logger
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    })
    return d
