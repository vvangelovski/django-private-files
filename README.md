# django-private-files

![Travis](https://img.shields.io/travis/vvangelovski/django-private-files.svg)

This application provides utilities for controlling access to static files based on
conditions you can specify within your Django application.
It provides a ``PrivatedFileField`` model field and appropriate signals for monitoring access to static content.
The basic goal is that you should be able to specify permissions for each ``PrivateFileField`` instance in
one method (or callable) and leave the rest to django-private-files.
Additionally you should be able to switch server (eg. from nginx to lighttpd) without hassle and remove
this application from your project without changes to your database.


It supports the following methods for limiting access to files:

* Basic - files are served with Python (not recommended for production if you have another choice)
* Nginx (X-Accel-Redirect) - you can specify protected locations within your nginx configuration file
* xsendfile - Apache (with mod_xsendfile), lighttpd and cherokee (not tested yet)


It's currently been tested with Django (1.9, 1.10, 1.11 and 2.0), Apache and Nginx. It should work with older
versions of django. Cherokee and lighttpd use the same mechanism as Apache mod_xsendfile, so
it should work, but it's not been tested or documented.

The full documentation for the project can be found on [Read the Docs](http://django-private-files.rtfd.org/)