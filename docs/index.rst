.. django-private-files documentation master file, created by
   sphinx-quickstart on Wed Mar 23 23:22:10 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================================
django-private-files 0.1.1 documentation
================================================

This application provides utilities for controlling access to static files based on
conditions you can specify within your Django application.
It provides a PrivatedFileField model field and appropriate signals for monitoring access to static content.
The basic goal is that you should be able to specify permissions for each PrivateFileField instance in
one method (or callable) and leave the rest to django-private-files.
Additionally you should be able to switch server (eg. from nginx to lighttpd) without hassle and remove
this application from your project without changes to your database.


It supports the following methods for limiting access to files:

   * Basic - files are served with Python (not recommended for production if you have another choice)
   * Nginx - you can specify protected locations within your nginx configuration file
   * xsendfile - Apache (with mod_xsendfile), lighttpd and cherokee (not tested yet)


It's currently been tested with Django 1.3, Apache, Nginx and Lighttpd. It should work with older versions of
django except for the example project. Cherokee uses the same mechanism as Apache mod_xsendfile and lighttpd, so
it should work, but it's not been tested or documented.


Contents:

.. toctree::
    :maxdepth: 2
    
    installation
    usage
    serverconf









Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

