from __future__ import absolute_import, unicode_literals

try:
    from django.apps import AppConfig

    class PrivateFilesConfig(AppConfig):
        name = 'private_files'
        verbose_name = 'Django Private Files'

except ImportError:  # pragma: no cover
    pass