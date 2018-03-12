#!/usr/bin/env python
import os
import sys
from django.core.management import call_command

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "private_files.tests.settings")

    import django
    django.setup()

    argv = list(sys.argv)
    argv.insert(1, 'test')
    call_command('test')

if __name__ == '__main__':
    main()