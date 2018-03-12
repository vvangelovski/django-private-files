#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "private_files.tests.settings")
    import django
    django.setup()

    from django.core.management import call_command
    from django.conf import settings
    try:
        settings.configure()
    except RuntimeError:
        pass
    call_command('test')

if __name__ == '__main__':
    main()