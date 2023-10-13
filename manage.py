#!/usr/bin/env python

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def init_django():
    import django
    from django.conf import settings

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=[
            'db',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'db.sqlite3'
                ),
            }
        },
        MEDIA_URL='/media/',
        MEDIA_ROOT=BASE_DIR / 'media'
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
