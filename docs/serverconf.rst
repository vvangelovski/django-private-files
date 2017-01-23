
Server configurations
======================

All of the bellow examples assume that:
    
    * ``MEDIA_ROOT`` is set to ``/media/psf/Home/Projects/django-private-files/testproject/static/``
    * ``MEDIA_URL`` is set to ``/media/``
    * Protected files are stored in two subfolders ``uploads`` and ``downloadables``
    * Other static files stored in ``MEDIA_ROOT`` should be freely downloadable
    

Apache
------------

If you serve your static content with Apache and have mod_xsendfile you can set ``FILE_PROTECTION_METHOD`` to ``xsendfile``. Turn
``XSendFile`` on and deny access to the directory where you store your protected files (the value of ``upload_to`` appended to ``MEDIA_ROOT``).
Here's an exmple of a vhost configuration with mod_xsendfile and mod_wsgi:


.. code-block:: apacheconf

		<VirtualHost *:80>
			ServerName django.test 
			XSendFile on
			alias /adminmedia/ /media/psf/Home/Projects/django-private-files/testproject/static/
			alias /media/ /home/vasil/src/django-trunk/django/contrib/admin/media/
			WSGIDaemonProcess django-test user=vasil group=users threads=1 processes=5
			WSGIProcessGroup django-test 
		  	WSGIScriptAlias / /media/psf/Home/Projects/django-private-files/testproject/django.wsgi
		  	
		  	<Directory /media/psf/Home/Projects/django-private-files/testproject>
		  	    Order deny,allow
		  	    Allow from all
		  	</Directory>
		  	
		  	<Directory /media/psf/Home/Projects/django-private-files/testproject/static/uploads>
		  	    Order deny,allow
		  	    Deny from all
		  	</Directory>
		  	
		  	<Directory /media/psf/Home/Projects/django-private-files/testproject/static/downloadables>
		  	    Order deny,allow
		  	    Deny from all
		  	</Directory>
		  	
		  	<Directory /home/vasil/src/django-trunk/django/contrib/admin>
		  	    Order deny,allow
		  	    Allow from all
		  	</Directory>
		    
		    ErrorLog /var/log/httpd/test.err.log
		</VirtualHost>


lighttpd
------------

Lighttpd has the same mechanism of controlling access to files from a proxy backend. The following example
proxies request to django running on fcgi:

.. code-block:: lighty


		$HTTP["host"] =~ "^django.test$" {
			server.errorlog = "/var/log/lighttpd/test-error.log"
			accesslog.filename = "/var/log/lighttpd/test-access.log"

			alias.url = (
		 	   "/adminmedia" => "/home/vasil/src/django-trunk/django/contrib/admin/media/",
		 	    "/media" => "/media/psf/Home/Projects/django-private-files/testproject/static/",
			)
			
			fastcgi.server = (
		 	   "/django.fcgi" => (
		        	"main" => (
		          	  # Use host / port instead of socket for TCP fastcgi
		        	"allow-x-send-file" => "enable", 
			   	 	"host" => "127.0.0.1",
		            "port" => 3033,
		            "check-local" => "disable",
		        	)
		    	),
			)
			
			url.access-deny = ( "/media/uploads/", "/media/downloadables/" )

			url.rewrite-once = (
		 		"^(/adminmedia.*)$" => "$1",
		 		"^(/media.*)$" => "$1",
				"^/django.fcgi(/.*)$" => "django.fcgi$1",
		    	"^(/.*)$" => "django.fcgi$1",
				)
		}


Nginx
-----------
If you use nginx to serve your static files you can set the ``internal`` directive like so:

.. code-block:: nginx

			http {
			    include       mime.types;
			    default_type  application/octet-stream;

			    sendfile        on;

				keepalive_timeout  65;


			    server {
			    listen   80;
			    server_name  django.test;

			    location /uploads/{
			     	internal;
			        root /media/psf/Home/Projects/django-private-files/testproject/static;
			    } 
			    
			    location /downloadables/{
    			     	internal;
    			     	root /media/psf/Home/Projects/django-private-files/testproject/static;
    			}
    			
    			
 			   location /media/ {
    			     	alias /media/psf/Home/Projects/django-private-files/testproject/static/;
    			}
                
                
 			   location /media/uploads/ {
 			        deny all;
 			    
 			    }
 			    
 			    
 			   location /media/downloadables/ {
 			        deny all;
 			    }

			    location /adminmedia {
			        alias   /home/vasil/src/django-trunk/django/contrib/admin/media;
			    }

			    location / {
			        # for a TCP host/port:
			         fastcgi_pass   localhost:3033;

			        # necessary parameter
			        fastcgi_param PATH_INFO $fastcgi_script_name;

				include fastcgi.conf;

			        # to deal with POST requests
			        fastcgi_param REQUEST_METHOD $request_method;
			        fastcgi_param CONTENT_TYPE $content_type;
			        fastcgi_param CONTENT_LENGTH $content_length;

			    }
			}	


