import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "private_files.tests.settings")
    #sys.path.insert(0, "tests")

    import django
    django.setup()

    argv = list(sys.argv)
    argv.insert(1, 'test')
    execute_from_command_line(argv)

if __name__ == '__main__':
    main()