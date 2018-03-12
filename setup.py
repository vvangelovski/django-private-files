from private_files import get_version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name = 'django-private-files',
    version = get_version(),
    packages = ['private_files', 'private_files.models'],
    author = 'Vasil Vangelovski',
    author_email = 'vvangelovski@gmail.com',
    license = 'New BSD License (http://www.opensource.org/licenses/bsd-license.php)',
    description = 'Protected files in django',
    url = 'https://github.com/vvangelovski/django-private-files',
    include_package_data = True,
    long_description = """
    =====================
    django-private-files
    =====================


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
    
    The full documentation for the project can be found on `Read the Docs <http://django-private-files.rtfd.org/>`_ .
    """,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
