Installation
==============

Install from PyPI with ``easy_install`` or ``pip``:

.. code-block:: bash

		pip install django-private-files

or download the source and do:

.. code-block:: bash

    	python setup.py install

or if you want to hack on the code symlink to it in your site-packages:

.. code-block:: bash

		python setup.py develop

In your settings.py ``INSTALLED_APPS`` add ``private_files``.
You must specify a protection method (``basic``, ``nginx`` or ``xsendfile``) in your settings.py

.. code-block:: python

    	FILE_PROTECTION_METHOD = 'basic'

In your urls.py add the ``private_files`` application urls:

.. code-block:: python

		from django.conf.urls.defaults import patterns, include, url

		# Uncomment the next two lines to enable the admin:
		from django.contrib import admin
		admin.autodiscover()

		urlpatterns = patterns('',
		    # Examples:
		    url(r'^private_files/', include('private_files.urls')),

		    # Uncomment the admin/doc line below to enable admin documentation:
		    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

		    # Uncomment the next line to enable the admin:
		    url(r'^admin/', include(admin.site.urls)),
		)
