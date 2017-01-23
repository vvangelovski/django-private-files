Usage
=========

Limiting Access to Static Files
----------------------------------

To protect a static file that you have reference to in the database you need
to use the ``PrivateFileField`` model field. For example::

		from django.db import models
		from private_files import PrivateFileField

		class FileSubmission(models.Model):
		    description = models.CharField("description", max_length = 200)
		    uploaded_file = PrivateFileField("file", upload_to = 'uploads')

By default it will check if the user is authenticated and let them download the
file as an attachment.

If you want to do more complex checks for the permission to download the file you
need to pass your own callable to the ``condition`` parameter::

		from django.db import models
		from django.contrib.auth.models import User
		from private_files import PrivateFileField

		def is_owner(request, instance):
		    return (not request.user.is_anonymous()) and request.user.is_authenticated and
				   instance.owner.pk = request.user.pk

		class FileSubmission(models.Model):
		    description = models.CharField("description", max_length = 200)
			owner = models.ForeignKey(User)
		    uploaded_file = PrivateFileField("file", upload_to = 'uploads', condition = is_owner)

This would check if the user requesting the file is the same user referenced in the ``owner`` field and
serve the file if it's true, otherwise it will throw ``PermissionDenied``.
``condition`` should return ``True`` if the ``request`` user should be able to download the file and ``False`` otherwise.

Another optional parameter is ``attachment``. It allows you to control wether the ``content-disposition`` header is sent or not.
By default it is ``True``, meaning the user will always be prompted to download the file by the browser.


Monitoring Access to Static Files
------------------------------------------

By using ``django-private-files`` you can monitor when a file is requested for download.
By hooking to the ``pre_download`` signal. This fires when a user is granted access to a file
and right before the server starts streaming the file to the user. The following is a simple
example of using the signal to provide a download counter::

    from django.db import models
    from django.contrib.auth.models import User
    from private_files import PrivateFileField, pre_download

    class CountedDownloads(models.Model):
        description = models.CharField("description", max_length = 200)
        downloadable = PrivateFileField("file", upload_to = 'downloadables')
        downloads = models.PositiveIntegerField("downloads total", default = 0)
    
    def handle_pre_download(instance, field_name, request, **kwargs):
        instance.downloads += 1
        instance.save()
    
    pre_download.connect(handle_pre_download, sender = CountedDownloads)